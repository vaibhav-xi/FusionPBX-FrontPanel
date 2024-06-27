from weasyprint import HTML

def client_pdf(details, company, street, plz, city, invoice_date, service_period, output):
    
    
    def generate_table(des_name, des_num, price_min, min, monthly_fee,
                       t_freecalls, t_freemins, total, min_og, total_calls,
                       price_pc, monthly_bool, freecall_bool, freemin_bool,
                       des_number):
        
        if freemin_bool:
        
            #available free mins
            if int(min_og) >= int(t_freemins):
                a_fmins = 0
                total = (int(min_og) - int(t_freemins)) * float(price_min)
            else:
                a_fmins = int(t_freemins) - int(min_og)
                total = 0
                
        if freecall_bool:
            
            #available free calls
            if int(total_calls) >= int(t_freecalls):
                a_fcalls = 0
                freecall_total = (int(total_calls) - int(t_freecalls)) * int(price_pc)
            else:
                a_fcalls = int(t_freecalls) - int(total_calls)
                freecall_total = 0.00
            
        des_total = "{:.2f}".format(total)
    
        
        if freecall_bool:
            freecall_total = "{:.2f}".format(freecall_total)
        else:
            freecall_total = 0
        
        if monthly_bool:
            monthly_fee = "{:.2f}".format(float(monthly_fee))
        else:
            monthly_fee = 0

        total += float(freecall_total) + float(monthly_fee)

        tax = "{:.2f}".format(total * 19/100)
        # grand_total = "{:.2f}".format(total + float(tax))
        grand_total = "{:.2f}".format(total)
        total = "{:.2f}".format(total)
        
        table_div = """"""
        
        table_part1 = f"""
            <div class="py-2">
                <div class="table-responsive">
                    <table class="table align-middle table-nowrap table-centered mb-0">
                        <thead>
                            <tr>
                                <th style="width: 70px;">Nr.</th>
                                <th>Ziel</th>
                                <th>Preis pro Minute</th>
                                <th>Minuten</th>
                                <th class="text-end" style="width: 120px;">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            
                            <tr>
                                <th scope="row">0{des_number}</th>
                                <td>
                                    <div>
                                        <h5 class="text-truncate font-size-14 mb-1">{des_name}</h5>
                                        <p class="text-muted mb-0">Zielrufnummer: {des_num}</p>
                                    </div>
                                </td>
                                <td>{price_min}€</td>
                                <td>{min}</td>
                                <td class="text-end">{des_total}€</td>
                            </tr>
                                            
            """
            
        table_part2 = f"""

            <tr>
                <th scope="row" colspan="4" class="text-end">Zwischensumme</th>
                <td class="text-end">{total}€</td>
            </tr>
        
        """
        
        table_div += table_part1
    
        if monthly_bool:
            
            row_month = f"""
            <tr>
                <th scope="row" colspan="4" class="text-end">Grundgebühr</th>
                <td class="text-end">{monthly_fee}€</td>
            <tr>
            """
        
            table_div += row_month
            
        if freecall_bool:
            
            row_free_calls = f"""
                                            
                <tr>
                    <th scope="row" colspan="4" class="text-end">Inklusivanrufer:</th>
                    <td class="text-end">{a_fcalls}/{t_freecalls}  {freecall_total}€</td>
                <tr>
            """
        
            table_div += row_free_calls
            
        if freemin_bool:
            
            row_free_mins = f"""
                                            
                <tr>
                    <th scope="row" colspan="4" class="text-end">Inklusivminuten:</th>
                    <td class="text-end"> {a_fmins}/{t_freemins}</td>
                <tr>
            """
            
            table_div += row_free_mins
        
        table_div += table_part2
        
        return table_div, grand_total
        
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="utf-8">


        <title>invoice card</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="/home/pi/fusion_panel/fusion_dashboard/dashboard/pdf_test/bootstrap.min.css" rel="stylesheet">
        <style type="text/css">
            body {{
                margin-top: 20px;
            }}
            
            .card {{
                box-shadow: 0 20px 27px 0 rgb(0 0 0 / 5%);
            }}
            
            .card {{
                position: relative;
                display: flex;
                flex-direction: column;
                min-width: 0;
                word-wrap: break-word;
                background-color: #fff;
                background-clip: border-box;
                border-radius: 1rem;
            }}
            
            @page {{size: 250mm 270mm;}}
            
        </style>
    </head>

    <body>
        <div class="container" style="border:none;">
            <div class="row" style="border:none;">
                <div class="col-lg-12" style="border:none;">
                    <div class="card" style="border:none;">
                        <div class="card-body" style="border:none;">
                            <div class="invoice-title">
                                <h4 class="float-end font-size-15" style="margin-right: -190px;">Rechnungsnummer #DS0204</h4>
                                
                                <div class="text-muted">
                                    <p class="mb-1">Innovicom GmbH <br> Zum Isetal 1 <br> 38518 Gifhorn</p>
                                </div>
                            </div>
                            <hr class="my-4">
                            <div class="row">
                                <div class="col-sm-6">
                                    <div class="text-muted">
                                        <h5 class="font-size-16 mb-3">Rechnung an:</h5>
                                        <h5 class="font-size-15 mb-2">{company}</h5>
                                        <p class="mb-1">{street}</p>
                                        <p class="mb-1">{plz}, {city}</p>
                                    </div>
                                </div>

                                <div class="col-sm-6">
                                    <div class="text-muted text-sm-end" style="float:right; margin-right:-40px; margin-top: -125px;">
                                        <div>
                                            <h5 class="font-size-10 mb-1">Rechnungsnummer:</h5>
                                            <p>#DZ0112</p>
                                        </div>
                                        <div class="mt-4">
                                            <h5 class="font-size-10 mb-1">Rechnungsdatum:</h5>
                                            <p>{invoice_date}</p>
                                        </div>
                                        <div class="mt-4">
                                            <h5 class="font-size-10 mb-1">Leistungszeitraum:</h5>
                                            <p>{service_period}</p>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            """
                                
    row_total = f"""
                                
                                <div class="d-print-none mt-4">
                                    <div class="float-end">
                                        <a href="javascript:window.print()" class="btn btn-success me-1"><i class="fa fa-print"></i></a>
                                        <a href="#" class="btn btn-primary w-md">Send</a>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            
                            <div style="display:flex;">
                                <div style="font-size: 10px;">
                                    Geschäftsführer: Tim Schulze
                                    <br>
                                    Ust.-IdNr.: DE 283265849
                                    
                                    <br>
                                    <br>
                                    
                                    Bankverbindung:
                                    <br>
                                    Sparkasse Hannover
                                    <br>
                                    IBAN: DE17 2505 0180 0910 1114 13
                                    <br>
                                    BIC/SWIFT: SPKHDE2HXXX
                                    <br>
                                </div>
                                
                                <div style="font-size: 10px; padding-left: 80px;">
                                    Innovicom GmbH
                                    <br>
                                    Zum Isetal 1,
                                    <br>
                                    38518 Gifhorn
                                    
                                    <br>
                                    <br>
                                    
                                    Tel: 0511 - 380 777 70
                                    <br>
                                    Fax: 0511 - 380 777 70
                                    <br>
                                    E-Mail: info@innovicom.de
                                    <br>
                                    Website: www.innovicom.de
                                    <br>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>

    </html>
    """
    
    des_number = 0
    g_total = 0
    
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
                        des_number)
        
        html_content += fun_return[0]
        g_total += float(fun_return[1])
        tax_total = "{:.2f}".format(g_total * 19/100)
        final_total = float(tax_total) + float(tax_total)
        
    table_final = f"""
                    <hr>

                    <tr>
                        <th scope="row" colspan="4" class="text-end">Zwischensumme</th>
                        <td class="text-end">{g_total}€</td>
                    </tr>

                    <tr>
                        <th scope="row" colspan="4" class="border-0 text-end">
                            MwSt. 19% </th>
                        <td class="border-0 text-end">{tax_total}€</td>
                    </tr>

                    <tr>
                        <th scope="row" colspan="4" class="border-0 text-end">Gesamtsumme</th>
                        <td class="border-0 text-end">
                            <h4 class="m-0 fw-semibold">{"{:.2f}".format(final_total)}€</h4>
                        </td>
                    </tr>

                </tbody>
            </table>
        </div>
        
        """
        
    html_content += table_final
    html_content += row_total

    # with open('invoice.html', 'w') as html_file:
    #     html_file.write(html_content)

    # # Use WeasyPrint to convert HTML to PDF
    # HTML('invoice.html').write_pdf('output.pdf')
    
    # print("GENERATING")

    # Save the modified HTML content to a file (e.g., invoice.html)
    with open('invoice.html', 'w') as html_file:
        html_file.write(html_content)

    # Use WeasyPrint to convert HTML to PDF
    HTML('invoice.html').write_pdf(f'/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/{output}.pdf')