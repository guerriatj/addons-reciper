def migrate(cr, version):
    cr.execute("""
        -- Désactiver certaines unités
        UPDATE uom_uom u
        SET active = FALSE
        FROM ir_model_data imd
        WHERE u.id = imd.res_id
        AND imd.module = 'uom'
        AND imd.name IN (
            'product_uom_millimeter',
            'product_uom_cm',
            'product_uom_cubic_inch',
            'product_uom_inch',
            'product_uom_oz',
            'product_uom_floz',
            'uom_square_foot',
            'product_uom_hour',
            'product_uom_foot',
            'product_uom_lb',
            'product_uom_yard',
            'product_uom_qt',
            'product_uom_day',
            'product_uom_meter',
            'uom_square_meter',
            'product_uom_gal',
            'product_uom_dozen',
            'product_uom_cubic_foot',
            'product_uom_km',
            'product_uom_ton',
            'product_uom_mile',
            'product_uom_cubic_meter'
        );

        UPDATE uom_uom u
        SET name = jsonb_set(COALESCE(u.name, '{}'::jsonb), '{en_US}', '"Litres"')
        FROM ir_model_data imd
        WHERE u.id = imd.res_id
        AND imd.module = 'uom'
        AND imd.name = 'product_uom_litre';

        UPDATE uom_uom u
        SET name = jsonb_set(COALESCE(u.name, '{}'::jsonb), '{en_US}', '"Grammes"')
        FROM ir_model_data imd
        WHERE u.id = imd.res_id
        AND imd.module = 'uom'
        AND imd.name = 'product_uom_gram';

        UPDATE uom_uom u
        SET name = jsonb_set(COALESCE(u.name, '{}'::jsonb), '{en_US}', '"Kilos"')
        FROM ir_model_data imd
        WHERE u.id = imd.res_id
        AND imd.module = 'uom'
        AND imd.name = 'product_uom_kgm';
    """)