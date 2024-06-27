# from weasyprint import HTML
import pdfkit

def gen_clientinvoice(details, company, street, plz, city,
                    invoice_date, service_period, output,
                    table_freemins, table_freecalls, table_monthly,
                    invoice_number):
    # table_monthly = False
    # table_freecalls = False
    # table_freemins = False
    
    # print(company, street, plz, city)
    
    def conv_ger(my_num):
        return str(my_num).replace(",", ".").replace(".", ",")

    def generate_table(des_name, des_num, price_min, min, monthly_fee,
                    t_freecalls, t_freemins, total, min_og, total_calls,
                    price_pc, monthly_bool, freecall_bool, freemin_bool,
                    des_number, table_monthly, table_freecalls,
                    table_freemins):
        
            # table_monthly = False
            # table_freecalls = False
            # table_freemins = False
            
            print("PASSED TOTAL: ", total, "FREE MIN: ", freemin_bool)
            
            print("DATA: ", (min_og / 60), int((min_og / 60)))
        
            if freemin_bool:
            
                #available free mins
                if float((min_og / 60)) >= float(t_freemins):
                    a_fmins = 0
                    total = (float((min_og / 60)) - float(t_freemins)) * float(str(price_min).replace(".", "").replace(",", "."))
                else:
                    a_fmins = float(t_freemins) - float((min_og / 60))
                    total = 0
                    
            if freecall_bool:
                
                #available free calls
                if int(total_calls) >= int(t_freecalls):
                    a_fcalls = 0
                    freecall_total = (int(total_calls) - int(t_freecalls)) * int(price_pc)
                else:
                    a_fcalls = int(t_freecalls) - int(total_calls)
                    freecall_total = 0.00
                
            des_total = conv_ger('{:,.2f}'.format(float("{:.2f}".format(total))))
        
            
            if freecall_bool:
                freecall_total = "{:.2f}".format(freecall_total)
            else:
                freecall_total = 0
            
            if monthly_bool:
                monthly_fee = "{:.2f}".format(float(monthly_fee))
            else:
                monthly_fee = 0

            total += float(freecall_total) + float(monthly_fee)
            
            # print("DETAILS: ", freecall_total, float(freecall_total), monthly_fee, float(monthly_fee))
            
            # print("TOTAL wit freecalls and monthly fee: ", total)
            
            monthly_fee = conv_ger('{:,.2f}'.format(float(monthly_fee)))

            tax = "{:.2f}".format(total * 19/100)
            # grand_total = "{:.2f}".format(total + float(tax))
            # grand_total = "{:.2f}".format(total)
            total = "{:.2f}".format(total)
            
            grand_total = conv_ger('{:,.2f}'.format(float(total)))
            
            price_min = conv_ger('{:,.2f}'.format(float(str(price_min).replace(".", "").replace(",", "."))))
        
            table_content = f"""    
                    <tr>
                    <th scope="row">{des_number}</th>
                    <td>{des_name}</td>
                    <td>{des_num}</td>
                    <td>{price_min}&euro;</td>
                """
                        
            # if freemin_bool:
            #     table_content += f"""<td>{a_fmins}/{t_freemins}</td>"""
                
            if table_freemins:
                if freemin_bool:
                    table_content += f"""<td>{a_fmins}/{t_freemins}</td>"""
                else:
                    table_content += f"""<td>0</td>"""
                
            if table_freecalls:
                if freecall_bool:
                    table_content += f"""<td>{a_fcalls}/{t_freecalls}</td>"""
                else:
                    table_content += f"""<td>0</td>"""
                
            # if freecall_bool or table_freecalls:
            #     table_content += f"""<td>0</td>"""
            
            freecall_total = conv_ger('{:,.2f}'.format(float(freecall_total)))
                        
                        
            table_content += f"""
                        <td>{conv_ger('{:,.2f}'.format((float(min_og) / 60)))}</td>
                        <td>{total_calls}</td>
                        <td>{des_total}&euro;</td>
                        <td>{freecall_total}&euro;</td>
                        """
                        
            # if monthly_bool:
            #     table_content += f"""<td>{monthly_fee}&euro;</td>"""
                
            if table_monthly:
                if monthly_bool:
                    table_content += f"""<td>{monthly_fee}&euro;</td>"""
                else:
                    table_content += f"""<td>0&euro;</td>"""
                        
            table_content += f"""<td>{grand_total}&euro;</td></tr>"""
            
            # print(f"""
                  
            #       {table_content}
                  
            #       """)
            
            return table_content, total
            
    html_content = f"""

    <html>

    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>

        <style>
            .my-header {{
                margin-top: 50px;
            }}
            
            .table {{
                width: 50px;
            }}
            
            .myinvoicenum {{
                float: right;
                margin-top: -108px;
            }}
            
            .table {{
                margin-top: 191px !important;
            }}
            
            .my-header2 {{
                margin-top: 60px;
            }}
            
            span.client_address {{
                margin-left: 37px;
            }}
            
            .myfotter {{
                display: flex;
                font-size: small;
            }}
            
            .p2 {{
                margin-left: 100px;
            }}
        </style>
        
        <meta charset="utf-8">
    </head>

    <body>

        <div class="containerr">

            <div class="my-header">
                <div class="myaddress">
                    Innovicom GmbH
                    <br> Zum Isetal 1
                    <br> 38518 Gifhorn
                </div>

                <div class="myinvoicenum">
                    Rechnungsnummer: #{invoice_number}
                </div>

            </div>

            <hr>

            <div class="my-header2">
                <div class="myaddress">
                    Rechnung an:
                    <br> <span class="client_address">{company}</span>
                    <br> <span class="client_address">{street}</span>
                    <br> <span class="client_address">{plz}, {city}</span>
                </div>

                <div class="myinvoicenum">
                    Rechnungsnummer: #{invoice_number}

                    <br> Rechnungsdatum: {invoice_date}

                    <br> Leistungszeitraum: {service_period}

                </div>

            </div>
            """

    thead2 = f"""
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th scope="col">Nr.</th>
                        <th scope="col">Ziel</th>
                        <th scope="col">Zielrufnummer</th>
                        <th scope="col">Preis pro Minute</th>
                        """
    thead3 = f"""                    
                        <th scope="col">Gesamt Minuten</th>
                        <th scope="col">Gesamt Anrufer</th>
                        <th scope="col">Kosten Minuten</th>
                        <th scope="col">Kosten Anrufer</th>
                        """
                        
    thead4 = f"""
                        <th scope="col">Kosten</th>
                    </tr>
                </thead>
                <tbody>
            """

    des_number = 0
    g_total = 0
    
    dynamic_html = """ """
    
    # table_monthly = False
    # table_freecalls = False
    # table_freemins = False
    
    table_num = 0

    for key in details:
        destination = details[key]
        des_number += 1
        
        fun_return = generate_table(destination["des_name"], destination["des_num"],
                        destination["price_min"], destination["min"],
                        destination["monthly_fee"],destination["t_freecalls"],
                        destination["t_freemins"], destination["total"],
                        destination["min_og"], destination["total_calls"],
                        destination["price_pc"], destination["monthly_bool"],
                        destination["freecall_bool"], destination["freemin_bool"],
                        des_number, table_monthly, table_freecalls, 
                        table_freemins)
        
        dynamic_html += fun_return[0]
        g_total += float(fun_return[1])
        
        # table_monthly = fun_return[2]
        # table_freecalls = fun_return[3]
        # table_freemins = fun_return[4]
        
    g_total = float(g_total)
    
    tax_total = float("{:.2f}".format(g_total * 19/100))
    final_total = conv_ger('{:,.2f}'.format(tax_total + g_total))
    
    tax_total = conv_ger('{:,.2f}'.format(float("{:.2f}".format(g_total * 19/100))))
    g_total = conv_ger('{:,.2f}'.format(g_total))
        
    if table_freemins:
        thead2 += """<th scope="col">inkl. Min.</th>"""
        table_num += 1
        
    if table_freecalls:
        thead2 += """<th scope="col">inkl. Anrufer</th>"""
        table_num += 1
        
    if table_monthly:
        thead3 += """<th scope="col">Grundgebühr</th>"""
        table_num += 1
        
    part2 = f"""
                    <tr>
                        <th scope="row"></th>
                        <td colspan="{8 + table_num}"></td>
                    </tr>

                    <tr>
                        <th scope="row"></th>
                        <td colspan="{6 + table_num}"></td>
                        <td>Zwischensumme:</td>
                        <td>{conv_ger(g_total)}&euro;</td>
                    </tr>
                    <tr>
                        <th scope="row"></th>
                        <td colspan="{6 + table_num}"></td>
                        <td>MwSt. 19%:</td>
                        <td>{conv_ger(tax_total)}&euro;</td>
                    </tr>
                    <tr>
                        <th scope="row"></th>
                        <td colspan="{6 + table_num}"></td>
                        <td>Gesamtsumme:</td>
                        <td>{conv_ger(final_total)}&euro;</td>
                    </tr>
                </tbody>
            </table>

            <hr>

            <div class="myfotter">
                <div class="p1">
                    Geschäftsführer: Tim Schulze
                    <br> Ust.-IdNr.: DE 283265849
                    <br> Bankverbindung:
                    <br> Sparkasse Hannover
                    <br> IBAN: DE17 2505 0180 0910 1114 13
                    <br> BIC/SWIFT: SPKHDE2HXXX
                </div>

                <div class="p2">
                    Innovicom GmbH
                    <br> Zum Isetal 1,
                    <br> 38518 Gifhorn
                    <br>
                    <br> Tel: 0511 - 380 777 70
                    <br> Fax: 0511 - 380 777 70
                    <br> E-Mail: info@innovicom.de
                    <br> Website: www.innovicom.de

                </div>
            </div>
        </div>
    </body>

    </html>

    """
        
    table_head = """"""
    table_head += thead2
    table_head += thead3
    table_head += thead4

    html_content += table_head
    html_content += dynamic_html
    html_content += part2

    # Save the modified HTML content to a file (e.g., invoice.html)
    with open('invoice.html', 'w') as html_file:
        html_file.write(html_content)

    # HTML('invoice.html').write_pdf(f'/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/test_invoice.pdf')

    pdfkit.from_file('invoice.html', f'/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/{output}.pdf')