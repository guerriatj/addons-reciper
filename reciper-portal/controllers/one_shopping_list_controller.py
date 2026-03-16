from odoo import http
from odoo.http import request
from datetime import date


class ShoppingWebController(http.Controller):
    @http.route('/my/shopping/list/new', type='http', auth='user', website=True)
    def create_shopping_list_page(self, **kw):
        shopping_list = request.env['shopping.list'].sudo().create({})
        return request.redirect(f"/my/view_shopping_list?shopping_list_id={shopping_list.id}")

    @http.route("/my/view_shopping_list", type='http', auth='user', website=True)
    def view_one_sopping_list(self, shopping_list_id=None, **kw):
        shopping_list = request.env['shopping.list'].sudo().browse(int(shopping_list_id))

        if shopping_list.state == "draft":
            return self.display_draft_shopping_list(shopping_list)
        else:
            return self.display_confirmed_shopping_list(shopping_list)


    def display_draft_shopping_list(self, shopping_list):
        recipes = request.env['recipe'].sudo().search([])
        ingredients = request.env['recipe.ingredient'].sudo().search([])
        uoms = request.env['uom.uom'].sudo().search([])
        stores = request.env['store'].sudo().search([])

        return request.render('reciper-portal.shopping_list_draft', {
            'shopping_list': shopping_list,
            'stores': stores,
            'recipes': recipes,
            'ingredients': ingredients,
            'uoms': uoms,
        })

    def display_confirmed_shopping_list(self, shopping_list):

        lines = request.env["shopping.list.line"].sudo().search(
            [("shopping_list_id", "=", shopping_list.id)],
        )

        return request.render(
            "reciper-portal.shopping_list_confirmed",
            {
                "shopping_list": shopping_list,
                "lines": lines,
            },
        )

        return request.render('reciper-portal.shopping_list_confirmed', {
            'shopping_list': shopping_list,
            'recipes': recipes,
            'ingredients': ingredients,
            'uoms': uoms,
        })

    @http.route("/my/shopping_list/post", type='http', auth='user', website=True, methods=['POST'])
    def post_shopping_list(self, shopping_list_id=None, **kw):
        shopping_list_id = request.params.get("shopping_list_id")
        shopping_list = request.env['shopping.list'].browse(int(shopping_list_id))
        form = request.httprequest.form

        shopping_list.create_recipe_lines(form)
        shopping_list.create_ingredient_lines(form)

        if kw.get("state") == "confirmed":
            shopping_list.action_generate_from_recipes()
            shopping_list.action_confirm()

        if kw.get("store_id"):
            shopping_list.write({"store_id": int(kw.get("store_id"))})

        return request.redirect(f"/my/view_shopping_list?shopping_list_id={shopping_list.id}")


    @http.route(
        "/shopping_list/toggle_line",
        type="json",
        auth="user",
        website=True,
    )
    def toggle_line(self, line_id):
        line = request.env["shopping.list.line"].sudo().browse(int(line_id))
        if not line.exists():
            return {"success": False}

        line.is_picked = not line.is_picked
        return {
            "success": True,
            "is_picked": line.is_picked,
        }

    #
    #
    # class ProofOfLifeController(CustomerPortal):
    #     @route(["/my/proof_of_life/form/<int:proof_of_life_id>"], type="http", auth="user", website=True)
    #     def proof_of_life_form(self, proof_of_life_id=None):
    #         return self.get_portal_response("ocb_website.ocb_proof_of_life_form",
    #                                         self.get_pol_value(proof_of_life_id, {}))
    #
    #     @route(["/my/shopping_list/post"], type="http", auth="user", website=True)
    #     def post_shopping_list(self, **post):
    #         proof_of_life = request.env["proof.of.life"]
    #         if post.get("proof_of_life_id"):
    #             proof_of_life = proof_of_life.browse(int(post.get("proof_of_life_id")))
    #             post.pop("proof_of_life_id")
    #
    #         question_values = []
    #         if post.get("question_count"):
    #             count = int(post.pop("question_count"))
    #             for question_count in range(0, count):
    #                 question = post.pop(f"question_{question_count}")
    #                 answer = post.pop(f"answer_{question_count}")
    #                 question_values.append((0, 0, {"question": question, "answer": answer, "pol_id": proof_of_life.id}))
    #
    #         if proof_of_life:
    #             self.update_existing_pol_lines(proof_of_life, post)
    #
    #         values = self.check_error_get_values(post, MANDATORY_POL_FIELDS, OPTIONNAL_POL_FIELDS, [])
    #         values.update(self.get_pol_value(proof_of_life.id, post))
    #         question_count = len(question_values)
    #         if proof_of_life:
    #             question_count += len(proof_of_life.pol_line_ids)
    #
    #         if post.get("state") != "draft":
    #             if not values.get("error"):
    #                 values["error"] = {}
    #                 values["error_message"] = []
    #             if not values.get("is_read_document"):
    #                 message = _(
    #                     "You need to tick the checkbox 'I have read and understood the Proof of Life Explanation Document'"
    #                 )
    #                 values["error"]["is_read_document"] = "error"
    #                 values["error_message"].append(message)
    #             if not question_count >= 5:
    #                 message = _("You need to have at least 5 questions")
    #                 values["error"]["question_count"] = "error"
    #                 values["error_message"].append(message)
    #
    #         values["proof_of_life"] = self.save_proof_of_life_values(proof_of_life, values, question_values)
    #         if values.get("error"):
    #             return self.get_portal_response("ocb_website.ocb_proof_of_life_form", values)
    #         else:
    #             return request.redirect("/my/home?uncollapse=pol")
    #
    #     def get_pol_value(self, proof_of_life_id, post):
    #         proof_of_life = request.env["proof.of.life"].browse(int(proof_of_life_id))
    #         is_read_document = (
    #             bool(
    #                 int(post.get("is_read_document"))) if "is_read_document" in post else proof_of_life.is_read_document
    #         )
    #         document = request.env.ref("ocb_document.documents_proof_of_life_pdf_document").sudo()
    #         values = {
    #             "proof_of_life": proof_of_life,
    #             "is_read_document": is_read_document,
    #             "page_name": "add_proof_of_life",
    #             "documents": document,
    #             "access_token": document.attachment_id.access_token,
    #         }
    #         return values
    #
    #     def save_proof_of_life_values(self, proof_of_life, values, question_values):
    #         # Create a copy of values to avoid modifying the original dict
    #         vals_to_save = values.copy()
    #         vals_to_save.pop("page_name", False)
    #         vals_to_save.pop("proof_of_life", False)
    #         vals_to_save.pop("documents", False)
    #         vals_to_save.pop("error", False)
    #         vals_to_save.pop("error_message", False)
    #         vals_to_save.pop("debug", False)
    #         vals_to_save.pop("access_token", False)
    #
    #         if proof_of_life:
    #             vals_to_save.pop("state")
    #             proof_of_life.sudo().write(vals_to_save)
    #         else:
    #             vals_to_save.update(
    #                 {
    #                     "user_id": request.env.user.id,
    #                     "state": "draft",
    #                 }
    #             )
    #             proof_of_life = request.env["proof.of.life"].sudo().create(vals_to_save)
    #         if question_values:
    #             proof_of_life.write({"pol_line_ids": question_values})
    #         return proof_of_life
    #
    #     def update_existing_pol_lines(self, proof_of_life, post):
    #         """Update existing POL lines based on POST data."""
    #         existing_line_updates = {}
    #         for key, value in list(post.items()):
    #             m_q = match(r"question_existing_(\d+)", key)
    #             m_a = match(r"answer_existing_(\d+)", key)
    #             if m_q:
    #                 line_id = int(m_q.group(1))
    #                 existing_line_updates.setdefault(line_id, {})["question"] = value
    #                 post.pop(key)
    #             if m_a:
    #                 line_id = int(m_a.group(1))
    #                 existing_line_updates.setdefault(line_id, {})["answer"] = value
    #                 post.pop(key)
    #         if existing_line_updates:
    #             for line_id, vals in existing_line_updates.items():
    #                 line = request.env["proof.of.life.line"].browse(line_id)
    #                 if line and line.pol_id.id == proof_of_life.id:
    #                     line.sudo().write(vals)
