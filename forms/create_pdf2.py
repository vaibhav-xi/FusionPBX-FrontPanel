from weasyprint import HTML

def generate_pdf(company, street, plz, city, des_name, des_num, price_min, min, total, output, credit):
    tax = "{:.2f}".format(total * 19/100)
    grand_total = "{:.2f}".format(total + float(tax))
    
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
                                            <p>12 Oct, 2020</p>
                                        </div>
                                        <div class="mt-4">
                                            <h5 class="font-size-10 mb-1">Leistungszeitraum:</h5>
                                            <p>#1123456</p>
                                        </div>
                                    </div>
                                </div>

                            </div>

                            <div class="py-2">
                                <h5 class="font-size-15">Zusammenfassung</h5>
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
                                                <th scope="row">01</th>
                                                <td>
                                                    <div>
                                                        <h5 class="text-truncate font-size-14 mb-1">{des_name}</h5>
                                                        <p class="text-muted mb-0">{des_num}</p>
                                                    </div>
                                                </td>
                                                <td>{price_min}€</td>
                                                <td>{min}</td>
                                                <td class="text-end">{total}€</td>
                                            </tr>
                                            
                                            <tr>
                                                <th scope="row" colspan="4" class="text-end">Monthly Fees: 100</th>
                                            <tr>
                                            
                                            <tr>
                                                <th scope="row" colspan="4" class="text-end">Total Credit: 50</th>
                                                <td class="text-end">Available Credit: 20</td>
                                            <tr>
                                            
                                            <tr>
                                                <th scope="row" colspan="4" class="text-end">Total Free Calls: 10</th>
                                                <td class="text-end">Available Free Calls: 1</td>
                                            <tr>
                                            
                                            <tr>
                                                <th scope="row" colspan="4" class="text-end">Total Free Mins: 30</th>
                                                <td class="text-end">Available Free Mins: 10</td>
                                            <tr>

                                            <tr>
                                                <th scope="row" colspan="4" class="text-end">Zwischensumme</th>
                                                <td class="text-end">{total}€</td>
                                            </tr>

                                            <tr>
                                                <th scope="row" colspan="4" class="border-0 text-end">
                                                    MwSt. 19% </th>
                                                <td class="border-0 text-end">{tax}€</td>
                                            </tr>

                                            <tr>
                                                <th scope="row" colspan="4" class="border-0 text-end">Gesamtsumme</th>
                                                <td class="border-0 text-end">
                                                    <h4 class="m-0 fw-semibold">{grand_total}€</h4>
                                                </td>
                                            </tr>

                                        </tbody>
                                    </table>
                                </div>
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