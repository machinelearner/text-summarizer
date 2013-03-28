$(function(){
    function para_number(para_id){
        var paraNumberPattern = /\d+/g;
        return para_id.match(paraNumberPattern);
    }
    var arrid=[];

    //$("p").hover(function(){
    //var html=$(this).html();
    //$(".content_summary").html(html);
    //});
    $(".para_container").hover(function(){
        var para_no = $(this).data("parano");
        var edits=$(this).find('#edits_' + para_no);
        var summary=$(this).find('#edits_summary_' + para_no);
        var edit_text = edits.text().trim();
        var summary_text = summary.text().trim();
        if(edit_text !="" && summary_text!=""){
        $(".comment_summary_wrapper").show()
        $("#edit_summary").html(summary.html());
        $("#edits").html(edits.html());
        var top= $(this).offset().top - 60;

        $(".comment_summary_wrapper").css("top",top);
        }
        else{
            $(".comment_summary_wrapper").hide()
        }
    });

    $("p").click(function(){
        var origianl_txt=$(this).text();
        //alert(origianl_txt);
        $(this).unbind("blur").bind("blur",function(){
            var edited_txt=$(this).text();
            //alert(edited_txt);
            if(origianl_txt==edited_txt){
                return false;
            } 
            else {//alert($(this).attr("id"));
                arrid.push($(this).attr("id"));
            }
        });
    });

    $("#save_comments_btn").click(function(){
        url = "/article/" + article_id + "/edit/save/";
        var para_edited = {};
        $.each(arrid, function(i, val){
            if($.inArray(val, para_edited) === -1) {
                console.log($(val).text());
                para_edited[para_number(val)] = $("#"+ val).text();
            }
        });
        $("p").removeAttr("contenteditable");
        $(".article").css("border","1px solid transparent");
        //alert(para_edited);
        $.get(url, {paragraphs : JSON.stringify(para_edited)}, function(response){
            //alert(response);
        });    });

        $("#edit_article_btn").click(function(){
            $("p").attr("contenteditable","true");
            $(".article").css("border","1px solid #cecece");
        });

        $("#article_summary_btn").click(function(){
            var maskHeight = $(document).height();
            var maskWidth = $(document).width();
            $('.overlay').css({'width':maskWidth,'height':maskHeight});
            $('.overlay').fadeIn(1000);   
            $('.overlay').fadeTo("slow",0.6);
            var winH = $(window).height();
            var winW = $(window).width();
            $(".article_summary_dialog").css('top',  winH/2-$(".article_summary_dialog").height()/2);
            $(".article_summary_dialog").css('left', winW/2-$(".article_summary_dialog").width()/2);
            $(".article_summary_dialog").fadeIn(1500); 
        })
        $('#close').click(function (e) {
            e.preventDefault();
            $('.overlay,.article_summary_dialog').hide();

        });
});
