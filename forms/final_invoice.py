# from weasyprint import HTML
import pdfkit
        
html_content = """

<html>

<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>

    <style>
        .my-header {
            margin-top: 50px;
        }
        
        .table {
            width: 50px;
        }
        
        .myinvoicenum {
            float: right;
            margin-top: -108px;
        }
        
        .table {
            margin-top: 191px !important;
        }
        
        .my-header2 {
            margin-top: 60px;
        }
        
        span.client_address {
            margin-left: 37px;
        }
        
        .myfotter {
            display: flex;
            font-size: small;
        }
        
        .p2 {
            margin-left: 100px;
        }
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
                Rechnungsnummer: #DS0204
            </div>

        </div>

        <hr>

        <div class="my-header2">
            <div class="myaddress">
                Rechnung an:
                <br> <span class="client_address">Test Company GmbH</span>
                <br> <span class="client_address">Zum Isetal 1</span>
                <br> <span class="client_address">Gifhorn, Germany</span>
            </div>

            <div class="myinvoicenum">
                Rechnungsnummer: #DZ0112

                <br> Rechnungsdatum: 07/12/2023

                <br> Leistungszeitraum: 01/12/2023 - 07/12/2023

            </div>

        </div>

        <table class="table table-sm">
            <thead>
                <tr>
                    <th scope="col">Nr.</th>
                    <th scope="col">Ziel</th>
                    <th scope="col">Zielrufnummer</th>
                    <th scope="col">Preis pro Minute</th>
                    <th scope="col">inkl. Min.</th>
                    <th scope="col">inkl. Anrufer</th>
                    <th scope="col">Gesamt Minuten</th>
                    <th scope="col">Gesamt Anrufer</th>
                    <th scope="col">Kosten Minuten</th>
                    <th scope="col">Kosten Anrufer</th>
                    <th scope="col">Grundgebühr</th>
                    <th scope="col">Kosten</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th scope="row">1</th>
                    <td>Destination 1</td>
                    <td>1253645321</td>
                    <td>0.9&euro;</td>
                    <td>0/20</td>
                    <td>0/50</td>
                    <td>30</td>
                    <td>60</td>
                    <td>10&euro;</td>
                    <td>50&euro;</td>
                    <td>500&euro;</td>
                    <td>500&euro;</td>
                </tr>
                <tr>
                    <th scope="row">2</th>
                    <td>Destination 2</td>
                    <td>1253645321</td>
                    <td>0.9&euro;</td>
                    <td>0/20</td>
                    <td>0/50</td>
                    <td>30</td>
                    <td>60</td>
                    <td>10&euro;</td>
                    <td>50&euro;</td>
                    <td>500&euro;</td>
                    <td>500&euro;</td>
                </tr>

                <tr>
                    <th scope="row"></th>
                    <td colspan="10"></td>
                </tr>

                <tr>
                    <th scope="row"></th>
                    <td colspan="8"></td>
                    <td>Zwischensumme:</td>
                    <td>100</td>
                </tr>
                <tr>
                    <th scope="row"></th>
                    <td colspan="8"></td>
                    <td>MwSt. 19%:</td>
                    <td>100</td>
                </tr>
                <tr>
                    <th scope="row"></th>
                    <td colspan="8"></td>
                    <td>Gesamtsumme:</td>
                    <td>100</td>
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

# Save the modified HTML content to a file (e.g., invoice.html)
with open('invoice.html', 'w') as html_file:
    html_file.write(html_content)

# HTML('invoice.html').write_pdf(f'/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/test_invoice.pdf')

pdfkit.from_file('invoice.html', f'/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/test_invoice.pdf')