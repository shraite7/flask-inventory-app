$(document).ready(function() {
    disableOptions();
    $("#productId").on("change", function(){
        $("#fromLocation option").not(":first").remove();
        if ($("#productId").val()) {
            ajaxCall("get-from-locations");
            enableOptions();
        } else {
            disableOptions();
        }
        return false;
    });
    
    $("#location_form").submit(function (e) {

        if (!$("#location_name").val()) {
          e.preventDefault();
          alert("Please fill the Location first");
        }
    });

    $("#product_form").submit(function (e) {
        if (!$("#product_name").val()) {
          e.preventDefault();
          alert("Please fill the Prodcut first");
        }
    });
    $("#movements_from").submit(function (e) {
        var msg = ''

        if (!$("#productId").val() || !$("#qty").val()) {
          msg += "Please fill the missing fields\n";
        }
        if (!$("#fromLocation").val() && !$("#toLocation").val()) {
          msg += "Please choose a warehouse\n";
        }

        if (
          parseInt($("#fromLocation option:selected").attr("data-max")) <
          parseInt($("#qty").val())
        ) {
          msg +=
            "Please Note that the quantity in the warehouse must be less than ( " +
            $("#fromLocation option:selected").attr("data-max") +
            " )";
        }

        if (msg) {
        e.preventDefault();
        alert(msg);
        }
    });
    
    if ($("#productId").val()) {
        enableOptions();
    }

    function enableOptions()
    {
        $("#qty").prop("disabled", false);
        $("#toLocation").prop("disabled", false);
        $("#fromLocation").prop("disabled", false);
    }

    function disableOptions()
    {
        $("#qty").prop("disabled", "disabled");
        $("#toLocation").prop("disabled", "disabled");
        $("#fromLocation").prop("disabled", "disabled");
    }

    function ajaxCall(table){
        $.ajax({
          data: {
            productId: $("#productId").val(),
            location: $("#fromLocation").val(),
          },
          type: "POST",
          url: table,
        }).done(function (data) {
          $.each(data, function (index,value){
              $("#fromLocation").append(
                $("<option>", {
                  value: index,
                  text: index,
                  "data-max": value.qty,
                })
              );
          });

        });
    }


});