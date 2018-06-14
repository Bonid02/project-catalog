var imageUrl;
var itemName;
var desc;
var quant;
var catId;
var itemId;

$(".link-category").click(function() {
    $("#output").empty();
    var catid = $(this).attr("id");
    var catName = $(this.children[0]).text();
    $("#category-name-title").text(catName);
    run_ajax_call(catid, "detailShow");
});


// Listener for close button inside modals
$(".close").click(function() {
    $("#item-detail-modal").hide();
    $("#item-addnew-modal").hide();
    $("#item-edit-modal").hide();
    $("#item-delete-modal").hide();
});

// Listener for add item link
$("#link-add-item").click(function() {
    $("#item-addnew-modal").show();
});


// Listener for button-edit
$(".button-edit").click(function() {
    $("#item-detail-modal").hide();
    $("#item-edit-modal").show();
    // assign the global vars to fields inside edit modal
    $("#item-imgurl-edit").val(imageUrl);
    $("#item-key-edit").val(itemId);
    $("#item-name-edit").val(itemName);
    $("#item-desc-edit").val(desc);
    $("#item-quant-edit").val(quant);
    $("#select-dropdown-edit").val(catId);
});

// Listener for delete item link
$(".button-delete").click(function() {
    $("#item-detail-modal").hide();
    $("#item-delete-modal").show();
    // assign the global vars to fields inside delete modal
    $("#item-img-del").attr("src", imageUrl);
    $("#item-key-del").val(itemId);
    $("#item-name-del").text(itemName);
    $("#item-desc-del").text(desc);
    $("#item-quant-del").text(quant);
    $("#item-cat-del").text(catName);
});


function run_ajax_call(categoryid, mode){
    $.ajax({
        url: "http://localhost:8000/category/"+categoryid,
        cache: false,
        success: function(results){
            for(var i = 0; i < results["Items"].length; i++) {
                obj_name = results["Items"];
                $("#output").append("<span id="+obj_name[i].id
                                    +" class='item-name'>"
                                    +obj_name[i].name+"</span></br>");
            }
            $(".item-name").click(function() {
                var itemid = $(this).attr("id");
                $.ajax({
                    url: "http://localhost:8000/item/"+itemid,
                    cache: false,
                    success: function(result){
                        imageUrl = result["Item"]["image_url"];
                        itemName = result["Item"]["name"];
                        desc = result["Item"]["description"];
                        catName = result["Item"]["cat_detail"]["name"];
                        quant = result["Item"]["quantity"];
                        catId = result["Item"]["category_id"];
                        itemId = result["Item"]["id"];
                        $("#item-img-modal").attr("src", imageUrl);
                        $("#item-name-modal").text(itemName);
                        $("#item-desc-modal").text(desc);
                        $("#item-cat-modal").text(catName);
                        $("#item-quantity-modal").text(quant);
                        if (mode == "edit") {
                            $("#item-detail-modal").show();
                        }
                    }
                });
                $("#item-detail-modal").show();
            });
        }
    });
}

function getCategoryName(){
    if ($("#category-name-title").text()) {
        cat_name = $("#category-name-title").text();
        menu_list = $(".menu-items-container").children();
        for(var i=0; i < menu_list.length; i++) {
            if (menu_list[i].children[0].innerText == cat_name) {
                categoryid = menu_list[i].id;
                run_ajax_call(categoryid, "add")
            }
        }
    }
}

// This will enable the refresh list everytime an Item is added or edited
getCategoryName();