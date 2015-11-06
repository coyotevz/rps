# -*- coding: utf-8 -*-

from os import path
from subprocess import call
import fpdf

cwd = path.abspath('.')

IMG_PATH = path.join(cwd, 'rps', 'static', 'img', 'logo_rp.png')
OUT_PATH = path.join(cwd, 'cupones')

class Cupon(fpdf.FPDF):

    customer = None

    def __init__(self, customer=None):
        super(Cupon, self).__init__(format='a5', orientation='P')
        if customer is not None:
            self.set_customer(customer)

    def set_customer(self, customer):
        self.customer = customer

    def print(self):
        assert self.customer is not None
        # 1. Create PDF
        self._create_pdf()
        # 2. Save PDF
        self._save_pdf()
        # 3. Print with lp
        return self._print_lp()

    def _create_pdf(self):
        self.add_page()
        self.image(IMG_PATH, x=45, w=58)
        self.set_font('Arial', '', 10)
        self.cell(128, h=5, ln=1)
        self._render_customer()
        self.line(0, 105, 148, 105)
        self.set_xy(10, 115)
        self._render_customer()

    def _render_customer(self):
        c = self.customer
        self.set_font('Arial', 'B', 35)
        self.cell(128, 25, txt='#{:0>4}'.format(c.id), ln=1, align='C')
        self.set_font('Arial', 'B', 25)
        self.cell(128, 20, txt='{}'.format(c.dni), ln=1, align='C')
        self.set_font('Arial', '', 25)
        self.cell(128, 20, txt='{} {}'.format(c.firstname, c.lastname),
                  ln=1, align='C')

    def _save_pdf(self):
        self._out_fn = path.join(OUT_PATH, 'c{:0>4}.pdf'.format(self.customer.id))
        self.output(self._out_fn, 'F')

    def _print_lp(self):
        retcode = call(["lp", "-o media=a5", self._out_fn])
        return bool(retcode)
