#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@Author: Vulkey_Chen (admin@gh0st.cn)
@Blog: https://gh0st.cn
@Data: 2019-04-25
@Team: Mystery Security Team (MSTSEC)
@Function: template
'''

main_html_template = '''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://bootswatch.com/4/darkly/bootstrap.min.css" crossorigin="anonymous">
        <title>SubDReporter Report for %s</title>
        <style type="text/css">
            a {
                color: rgb(52, 152, 219) !important;
            }

            a.badge {
                color: inherit !important;
            }

            footer {
                margin-top: 20px;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: rgb(68, 68, 68);
            }

            footer a {
                color: inherit !important;
                text-decoration: underline;
            }

            .logo {
                padding-left: 30px;
                padding-top: 10px;
                font-weight: bold;
                font-size: 16px;
            }

            .cluster {
                border-bottom: 1px solid rgb(68, 68, 68);
                padding: 30px 20px 20px 20px;
                overflow-x: auto;
                white-space: nowrap;
            }

            .cluster:nth-child(even) {
                background-color: rgba(0, 0, 0, 0.075);
                box-shadow: inset 0px 6px 8px rgb(24, 24, 24);
            }

            .page {
                display: inline-block;
                margin: 10px;
                width: 470px;
                overflow: hidden;
                box-shadow: 10px 10px 8px rgb(24, 24, 24);
            }

            .page .card-text {
        white-space: normal;
      }

            .page .screenshot-container {
              position: relative;
              width: 470px;
              height: 293px;
              overflow: hidden;
            }

            .page .screenshot-container img.screenshot {
              position: absolute;
              top: 0;
              left: 0;
              width: 100%%;
              height: 100%%;
              background-repeat: no-repeat;
              background-position: center;
              background-size: cover;
              transition: transform .5s ease-out;
            }

            .page .response-headers-container {
                display: none;
            }

            table.response-headers td {
                font-family: Anonymous Pro,Consolas,Menlo,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New,monospace,serif;
            }

            table.response-headers tr.insecure td {
                color: #E74C3C;
                font-weight: bold;
            }

            table.response-headers tr.secure td {
                color: rgb(0, 188, 140);
                font-weight: bold;
            }

            img.screenshot {
                transition: transform .2s ease-out;
            }

            img.no-screenshot {
                cursor: not-allowed;
            }
        </style>
    </head>
    <body>
        <pre class="logo">
   _____       __    ____  ____                        __           
  / ___/__  __/ /_  / __ \\/ __ \\___  ____  ____  _____/ /____  _____
  \\__ \\/ / / / __ \\/ / / / /_/ / _ \\/ __ \\/ __ \\/ ___/ __/ _ \\/ ___/
 ___/ / /_/ / /_/ / /_/ / _, _/  __/ /_/ / /_/ / /  / /_/  __/ /    
/____/\\__,_/_.___/_____/_/ |_|\\___/ .___/\\____/_/   \\__/\\___/_/     
                                 /_/ report for %s
        </pre>
        %s <!--table-->

        %s <!--footer-->
    </body>
</html>
'''

body_html_template = '''
<div class="cluster">
%s
</div>
'''

table_html_template = '''
        <div class="page card mb-3">
            <div class="card-body">
                <h5 class="card-title">%s</h5><!--url-->
                <a href="#" class="badge badge-pill badge-info">Status Code: %s</a><!--status_code-->
            </div>
            
                <div class="screenshot-container">
                    <a href="%s" target="_blank"><img src="%s" alt="" width="470" class="screenshot" /></a><!--screenshot-->
                </div>
            
            <div class="card-footer text-muted">
                <a href="#" class="card-link page-details-link">Details</a>
                <a href="%s" target="_blank" class="card-link page-visit-link">Visit</a><!--url-->
            </div>
            <div class="response-headers-container">
                <table class="table table-responsive table-striped table-hover table-sm response-headers">
                    <thead class="thead-dark">
                        <tr>
                            <th scope="col">Header</th>
                            <th scope="col">Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        %s
                    </tbody><!--header-->
                </table>
            </div>
        </div>
'''

header_html_template = '''
<tr>
    <td>%s</td>
    <td>%s</td>
</tr>
'''

footer_html_template = '''
<footer>
    <p>SubDReporter v0.2</p>
</footer>
<div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" id="details_modal">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
        <h5 class="modal-title"></h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button>
    </div>
    <div class="modal-body"></div>
    <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    </div>
        </div>
    </div>
</div>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
<script type="text/javascript">
    $(function() {
        $(".screenshot-container").on("mouseover", function() {
          $(this).find("img.screenshot").css({"transform": "scale(2)"});
        }).on("mouseout", function() {
          $(this).find("img.screenshot").css({"transform": "scale(1)"})
        }).on("mousemove", function(e) {
          $(this).find("img.screenshot").css({'transform-origin': ((e.pageX - $(this).offset().left) / $(this).width()) * 100 + '% ' + ((e.pageY - $(this).offset().top) / $(this).height()) * 100 +'%'});
        });

        $(".page-details-link").on("click", function(e) {
            e.preventDefault();
            var page    = $(this).closest(".page");
            var url     = page.find("h5.card-title").text();
            var headers = page.find(".response-headers-container").html();
            $("#details_modal .modal-header h5").text(url);
            $("#details_modal .modal-body").html(headers);
            $("#details_modal").modal();
        });
    });
</script>
'''



