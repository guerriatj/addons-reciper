/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

/**
 * Tronc commun pour les popups de galerie de recettes (photo + filtre par
 * nom). Ne fait rien de spécifique au clic sur une recette : les widgets
 * concrets (sélection multiple, consultation) héritent de cette classe et
 * surchargent _onGalleryItemClick / _onGalleryShow / _onGalleryHidden.
 */
export const RecipeGalleryWidget = publicWidget.Widget.extend({
    // Sélecteur du modal de galerie au sein de `this.el`. Un seul modal de ce
    // type par page.
    gallerySelector: '.recipe-gallery-modal',

    events: {
        'input .recipe-gallery-filter': '_onGalleryFilter',
        'click .recipe-gallery-item': '_onGalleryItemClick',
    },

    start() {
        const def = this._super(...arguments);
        this.galleryModalEl = this.el.querySelector(this.gallerySelector);
        if (this.galleryModalEl) {
            this.galleryModalEl.addEventListener('show.bs.modal', () => this._onGalleryShow());
            this.galleryModalEl.addEventListener('hidden.bs.modal', () => this._onGalleryHidden());
        }
        return def;
    },

    _onGalleryFilter(ev) {
        const query = ev.target.value.trim().toLowerCase();
        const modal = ev.target.closest(this.gallerySelector);
        modal.querySelectorAll('.recipe-gallery-item').forEach(item => {
            const name = (item.dataset.recipeName || '').toLowerCase();
            item.classList.toggle('d-none', query.length > 0 && !name.includes(query));
        });
    },

    // À surcharger.
    _onGalleryItemClick(ev) {},
    _onGalleryShow() {},

    _onGalleryHidden() {
        const filterInput = this.galleryModalEl.querySelector('.recipe-gallery-filter');
        if (filterInput) {
            filterInput.value = '';
            filterInput.dispatchEvent(new Event('input'));
        }
    },
});

/**
 * Mode "consultation" : clic sur une recette -> popup de détail
 * (photo / ingrédients / instructions).
 */
publicWidget.registry.recipe_gallery_view = RecipeGalleryWidget.extend({
    selector: '.o_recipe_gallery_view',

    start() {
        const def = this._super(...arguments);
        const detailModalEl = this.el.querySelector('#recipe_detail_modal');
        if (detailModalEl) {
            // Bootstrap retire `modal-open` du body à la fermeture d'un modal,
            // même si un autre (ici la galerie) reste ouvert derrière : on le
            // remet pour garder le scroll verrouillé et la galerie utilisable.
            detailModalEl.addEventListener('hidden.bs.modal', () => {
                if (this.galleryModalEl && this.galleryModalEl.classList.contains('show')) {
                    document.body.classList.add('modal-open');
                }
            });
        }

        // Deux modals Bootstrap superposés se disputent le focus (le mécanisme
        // interne de Bootstrap qui base l'écoute d'Échap sur l'élément
        // actuellement focus n'est pas fiable dans ce cas) : on gère nous-même
        // la touche Échap en priorité (capture), pour fermer uniquement le
        // popup de détail quand les deux sont ouverts.
        document.addEventListener('keydown', (ev) => this._onGalleryEscape(ev), true);

        return def;
    },

    _onGalleryEscape(ev) {
        if (ev.key !== 'Escape') return;
        const detailModalEl = this.el.querySelector('#recipe_detail_modal');
        if (detailModalEl && detailModalEl.classList.contains('show')) {
            ev.stopPropagation();
            window.Modal.getOrCreateInstance(detailModalEl).hide();
        }
    },

    async _onGalleryItemClick(ev) {
        const recipeId = parseInt(ev.currentTarget.dataset.recipeId, 10);
        if (!recipeId) return;

        const detail = await rpc('/my/recipe/detail', { recipe_id: recipeId });
        if (!detail) return;

        this._populateRecipeDetail(detail);

        // Superposé au modal de galerie (qui reste ouvert en arrière-plan).
        const detailModalEl = this.el.querySelector('#recipe_detail_modal');
        window.Modal.getOrCreateInstance(detailModalEl).show();
    },

    _populateRecipeDetail(detail) {
        const modal = this.el.querySelector('#recipe_detail_modal');

        modal.querySelector('.recipe-detail-name').textContent = detail.name || '';

        const img = modal.querySelector('.recipe-detail-img');
        const placeholder = modal.querySelector('.recipe-detail-img-placeholder');
        if (detail.image_url) {
            img.src = detail.image_url;
            img.classList.remove('d-none');
            placeholder.classList.add('d-none');
        } else {
            img.classList.add('d-none');
            placeholder.classList.remove('d-none');
            placeholder.textContent = detail.name ? detail.name[0].toUpperCase() : '?';
        }

        const ingredientsEl = modal.querySelector('.recipe-detail-ingredients');
        ingredientsEl.innerHTML = '';
        (detail.ingredients || []).forEach(ingredient => {
            const col = document.createElement('div');
            col.className = 'col-6 recipe-detail-ingredient';
            col.textContent = [ingredient.quantity, ingredient.uom, ingredient.name]
                .filter(Boolean)
                .join(' ');
            ingredientsEl.appendChild(col);
        });

        modal.querySelector('.recipe-detail-instructions').innerHTML = detail.instructions || '';
    },
});
