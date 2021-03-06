from test_plus.test import TestCase
from . import factories
from wallets import forms
from wallets import api
import mock


class TestWithdrawForm(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.bcy = factories.BcyFactory(user=self.user)

    def test_amount_field_label(self):
        form = forms.WithdrawForm()
        self.assertEqual(
            form.fields['amount'].label,
            None
        )

    def test_amount_field_help_text(self):
        form = forms.WithdrawForm()
        self.assertEqual(
            form.fields['amount'].help_text,
            ''
        )

    def test_amount_field_with_invalid_data(self):
        form_data = {'amount': 0}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            '* Amount must be greater than zero.'
        )

        form_data = {'amount': True}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            '* Enter a number.'
        )

        form_data = {'amount': 'string'}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            '* Enter a number.'
        )

    def test_amount_field_with_valid_data(self):
        form_data = {'amount': 1.0}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

        form_data = {'amount': '1.0'}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

        form_data = {'amount': 1}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

        form_data = {'amount': '1'}
        form = forms.WithdrawForm(data=form_data)
        error = form['amount'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

    def test_address_field_label(self):
        form = forms.WithdrawForm()
        self.assertEqual(
            form.fields['address'].label,
            None
        )

    def test_address_field_help_text(self):
        form = forms.WithdrawForm()
        self.assertEqual(
            form.fields['address'].help_text,
            ''
        )

    def test_address_field_with_invalid_data(self):
        form_data = {'address': 0}
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            '* Number of characters must be greater than 10.'
        )
        form_data = {'address': True}
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            '* Number of characters must be greater than 10.'
        )
        import random
        import string
        length = forms.WithdrawForm().fields['address'].max_length
        string = ''.join(
            random.choice(string.ascii_uppercase +
                          string.digits) for _ in range(length + 1))

        form_data = {'address': string}
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            '* Ensure this value has at most ' +
            '{} characters (it has {}).'.format(
                length,
                length + 1
            )
        )

        form_data = {'address': string}
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            '* Ensure this value has at most ' +
            '{} characters (it has {}).'.format(
                length,
                length + 1
            )
        )

        obj = factories.BcyFactory()
        form_data = {'address': obj.address}
        form = forms.WithdrawForm(data=form_data, obj=obj)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            '* The recipient\'s address and ' +
            'the sender\'s address must be different.'
        )

    def test_address_field_with_valid_data(self):
        obj = factories.BcyFactory()
        form_data = {'address': 'CvuiwCe7WZ8eD4P7ZNRs6zEU3K2okdNYm95'}
        form = forms.WithdrawForm(data=form_data, obj=obj)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

        form_data = {'address': 'CvuiwCe7WZ8eD4P7ZNRs6zEU3K2okdNYm95'}
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )

    def test_spend_with_obj(self):
        obj = factories.BcyFactory()
        api.not_simple_spend = mock.MagicMock(
            return_value='7981c7849294648c1e79dd16077a388' +
                         'b808fcf8c20035aec7cc5315b37dacfee')
        form_data = {
            'address': 'BvuiwCe7WZ8eD4P7ZNRs6zEU3K2okdNYm97',
            'amount': 0.25
        }
        form = forms.WithdrawForm(data=form_data, obj=obj)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )
        transaction = form.spend()
        self.assertEqual(
            transaction,
            '7981c7849294648c1e79dd16077a388b808fcf8c20035aec7cc5315b37dacfee'
        )

    def test_spend_without_obj(self):
        api.not_simple_spend = mock.MagicMock(
            return_value='7981c7849294648c1e79dd16077a388b' +
                         '808fcf8c20035aec7cc5315b37dacfee')
        form_data = {
            'address': 'BvuiwCe7WZ8eD4P7ZNRs6zEU3K2okdNYm97',
            'amount': 0.25
        }
        form = forms.WithdrawForm(data=form_data)
        error = form['address'].errors
        self.assertEqual(
            error.as_text(),
            ''
        )
        transaction = form.spend()
        self.assertEqual(
            transaction,
            None
        )

"""
class TestPayForm(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.bcy = factories.BcyFactory(user=self.user)
        self.invoice = factories.BcyInvoiceFactory(
            wallet=self.bcy,
        )
        self.payment = factories.PaymentBcyInvoiceFactory(
            invoice=self.invoice
        )
        self.form = forms.PayForm()

    def test_form_success_without_data(self):
        form = forms.PayForm(data={})
        self.assertTrue(form.is_valid())

    def test_form_valid_with_any_data(self):
        form = forms.PayForm(data={'data': 'data'})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = forms.PayForm(data={'asdasdasdasd'})
        print(form)
    '''
    def test_payload_field_label(self):
        self.assertEqual(
            self.form.fields['payload'].label,
            None
        )

    def test_payload_field_help_text(self):
        self.assertEqual(
            self.form.fields['payload'].help_text,
            ''
        )
    '''
    '''
    def test_payload_field_with_valid_data(self):

        import json
        data = json.dumps({
            'membership_id': 1
        })
        form_data = {
            'payload': data
        }
        form = forms.PayForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['payload'],
            data
        )

        data = ''
        form_data = {'payload': data}
        form = forms.PayForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue('payload' in form.cleaned_data)
        self.assertEqual(
            form.cleaned_data['payload'],
            ''
        )

        form_data = {
            'payload': {}
        }
        form = forms.PayForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['payload'],
            ''
        )

    def test_paylaod_field_with_invalid_data(self):
        data = '1 1232 13 123123'
        form_data = {'payload': data}
        form = forms.PayForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFalse('payload' in form.cleaned_data)
        error = form['payload'].errors
        self.assertEqual(
            error.as_text(),
            '* Invalid data in payload field.'
        )
    '''
"""