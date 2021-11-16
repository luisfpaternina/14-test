odoo.define('sat_companies_sale.javascript', ['web.ajax'], function(require){

    "use strict";

    var ajax = require('web.ajax');
    var button_sig_upload = document.getElementById("upload_signature")
    var button_dowload_contract = document.getElementById("preview_sale_contract")

    $(document).ready(function (){
        var container = document.getElementById("contract_test");

        if (container){
            container.innerHTML = "";
            container.innerHTML = "<div class='col text-center'>Cargando</div>";

            ajax.jsonRpc('/get_sale', 'call', {}).then(function(data){
                container.innerHTML = "";
                console.log(data)
                for (var i=0; i < data.length; i++){
                    container.innerHTML += '<h6 class="text-center mt-3 pb-1">' + data[i].name + '</h6>';
                }
                
            });

        }
    });

    

    button_sig_upload.onclick = function () {
        console.log('1')
        var c = document.getElementsByClassName("jSignature");
        console.log('2')
        var ctx = c.getContext("2d");
        ctx.fillRect(10, 10, 50, 50);
        console.log('3')
        function copy() {
            var imgData = ctx.getImageData(10, 10, 50, 50);
            ctx.putImageData(imgData, 10, 70);
        }
        console.log('test sample')
        var text_input = document.getElementById("formGroupExampleInput").value
        console.log('test  2')
        //var image_signature = document.getElementsByClassName("jSignature")
        //var context = image_signature.getContext('2d');

        console.log(text_input)

        ajax.jsonRpc('/send_sale', 'call', {text_input: text_input});
    
    };

    button_dowload_contract.onclick = function () {
        console.log("TEST  BUTTON DOWLOAD")
        var id_sale = document.getElementById("id_value_sale").textContent;
        ajax.jsonRpc('/get_sale/print_report_contract/', 'call', {id_sale: id_sale});
    
    };




});