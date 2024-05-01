import unittest

from odoo.addons.payment.tests.common import PaymentAcquirerCommon

import odoo
from odoo import fields
from odoo.tools import mute_logger


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class StripeCommon(PaymentAcquirerCommon):

    def setUp(self):
        super().setUp()
        self.stripe = self.env.ref("payment.payment_acquirer_stripe")


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class StripeTest(StripeCommon):

    @unittest.skip("Stripe test disabled: We do not want to overload Stripe with runbot's requests")
    def test_10_stripe_s2s(self):
        self.assertEqual(self.stripe.environment, "test", "test without test environment")

        # Add Stripe credentials
        self.stripe.write(
            {
                "stripe_secret_key": "sk_test_bldAlqh1U24L5HtRF9mBFpK7",
                "stripe_publishable_key": "pk_test_0TKSyYSZS9AcS4keZ2cxQQCW",
            }
        )

        # Create payment meethod for Stripe
        payment_token = self.env["payment.token"].create(
            {
                "acquirer_id": self.stripe.id,
                "partner_id": self.buyer_id,
                "cc_number": "4242424242424242",
                "cc_expiry": "02 / 26",
                "cc_brand": "visa",
                "cvc": "111",
                "cc_holder_name": "Johndoe",
            }
        )

        # Create transaction
        tx = self.env["payment.transaction"].create(
            {
                "reference": "test_ref_%s" % fields.date.today(),
                "currency_id": self.currency_euro.id,
                "acquirer_id": self.stripe.id,
                "partner_id": self.buyer_id,
                "payment_token_id": payment_token.id,
                "type": "server2server",
                "amount": 115.0,
            }
        )
        tx.stripe_s2s_do_transaction()

        # Check state
        self.assertEqual(tx.state, "done", "Stripe: Transcation has been discarded.")

    @unittest.skip("Stripe test disabled: We do not want to overload Stripe with runbot's requests")
    def test_20_stripe_form_render(self):
        self.assertEqual(self.stripe.environment, "test", "test without test environment")

        # ----------------------------------------
        # Test: button direct rendering
        # ----------------------------------------

        # render the button
        res = self.stripe.render("SO404", 320.0, self.currency_euro.id, values=self.buyer_values).decode("utf-8")
        popup_script_src = 'script src="https://checkout.stripe.com/checkout.js"'
        # check form result
        self.assertIn(popup_script_src, res, "Stripe: popup script not found in template render")
        # Generated and received
        self.assertIn(
            self.buyer_values.get("partner_email"), res, "Stripe: email input not found in rendered template"
        )

    @unittest.skip("Stripe test disabled: We do not want to overload Stripe with runbot's requests")
    def test_30_stripe_form_management(self):
        self.assertEqual(self.stripe.environment, "test", "test without test environment")

        # typical data posted by Stripe after client has successfully paid
        stripe_post_data = {
            "amount": 4700,
            "amount_refunded": 0,
            "application_fee": None,
            "balance_transaction": "txn_172xfnGMfVJxozLwssrsQZyT",
            "captured": True,
            "created": 1446529775,
            "currency": "eur",
            "customer": None,
            "description": None,
            "destination": None,
            "dispute": None,
            "failure_code": None,
            "failure_message": None,
            "fraud_details": {},
            "id": "ch_172xfnGMfVJxozLwEjSfpfxD",
            "invoice": None,
            "livemode": False,
            "metadata": {"reference": "SO100"},
            "object": "charge",
            "paid": True,
            "receipt_email": None,
            "receipt_number": None,
            "refunded": False,
            "refunds": {
                "data": [],
                "has_more": False,
                "object": "list",
                "total_count": 0,
                "url": "/v1/charges/ch_172xfnGMfVJxozLwEjSfpfxD/refunds",
            },
            "shipping": None,
            "source": {
                "address_city": None,
                "address_country": None,
                "address_line1": None,
                "address_line1_check": None,
                "address_line2": None,
                "address_state": None,
                "address_zip": None,
                "address_zip_check": None,
                "brand": "Visa",
                "country": "US",
                "customer": None,
                "cvc_check": "pass",
                "dynamic_last4": None,
                "exp_month": 2,
                "exp_year": 2022,
                "fingerprint": "9tJA9bUEuvEb3Ell",
                "funding": "credit",
                "id": "card_172xfjGMfVJxozLw1QO6gYNM",
                "last4": "4242",
                "metadata": {},
                "name": "norbert.buyer@example.com",
                "object": "card",
                "tokenization_method": None,
            },
            "statement_descriptor": None,
            "status": "succeeded",
        }

        tx = self.env["payment.transaction"].create(
            {
                "amount": 4700,
                "acquirer_id": self.stripe.id,
                "currency_id": self.currency_euro.id,
                "reference": "SO100",
                "partner_name": "Norbert Buyer",
                "partner_country_id": self.country_france.id,
            }
        )

        # validate it
        tx.form_feedback(stripe_post_data, "stripe")
        self.assertEqual(tx.state, "done", "Stripe: validation did not put tx into done state")
        self.assertEqual(tx.acquirer_reference, stripe_post_data.get("id"), "Stripe: validation did not update tx id")
        # reset tx
        tx.write({"state": "draft", "date_validate": False, "acquirer_reference": False})
        # simulate an error
        stripe_post_data["status"] = "error"
        stripe_post_data.update(
            {
                "error": {
                    "message": "Your card's expiration year is invalid.",
                    "code": "invalid_expiry_year",
                    "type": "card_error",
                    "param": "exp_year",
                }
            }
        )
        with mute_logger("odoo.addons.payment_stripe.models.payment"):
            tx.form_feedback(stripe_post_data, "stripe")
        # check state
        self.assertEqual(tx.state, "error", "Stipe: erroneous validation did not put tx into error state")
