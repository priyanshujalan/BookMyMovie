from fpdf import FPDF

class PDF(FPDF):
    def print_bill(self, s_name, v_name, tkts, d_t, user):
        self.set_y(50)
        self.set_font('Arial', 'B', 20)
        self.cell(0,0, v_name, 0, 0, 'C')
        
        content = "Movie: "+s_name+"\nDate & Time: "+d_t
        tickets = "\nTickets: " + tkts
        
        self.ln(10)
        self.set_font('Arial', '',12)
        self.multi_cell(0,7, "Booked By: "+user, 0)
        self.multi_cell(0,7, content, 0)
        self.multi_cell(0,7, tickets, 0)
        return 



    

