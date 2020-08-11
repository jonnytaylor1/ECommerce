//When the quantity input changes value, the
//change quantity button is programmatically clicked
//so that the new quantity is submitted
$('.quantity').change(function(event){
    $(event.target).next('.changeQuantity').click();
 });
