$(document).ready(function(){
    $("#correct").click(function(event){
        var label;
        label = $(this).attr("value");
        $('#success').fadeIn(500, function() {
        $(this).fadeOut(1000);
        });
        $.get("/tagging/label/", {label_instance_id: $("#instance_id").val(), flag:'1'}, function(data){
            update_page(data);
        });
    });

    $("#wrong").click(function(event){
        var label;
        label = $(this).attr("value");
        $('#success').fadeIn(500, function() {
        $(this).fadeOut(1000);
        });
        $.get("/tagging/label/", {label_instance_id: $("#instance_id").val(), flag:'2'}, function(data){
            update_page(data);
        });
    });

    $("#unknow").click(function(event){
        var label;
        label = $(this).attr("value");
        $.get("/tagging/label/", {label_instance_id: $("#instance_id").val(), flag:'0'}, function(data){
            update_page(data);
        });
    });
});

function update_page(data){
    if(data["finished"])
    {
        window.location.href = "/tagging/";
    }
    else
    {
        record = data["record"];
        ps = data["ps"];
        eventType = data["eventType"];
        subType = data["subType"];
        actor1 = data["actor1"];
        actor2 = data["actor2"];
        eventDate = data["date"];
        title = data["title"];
        ps = data["ps"];
        instanceId = data["instanceId"];
        remaind_count = data["remaind_count"];
        user_label_count = data["user_label_count"];

        $("#actor1").html(actor1);
        $("#actor2").html(actor2);
        $("#eventType").html(eventType);
        $("#subType").html(subType);
        $("#title").html('<h4>' + title + '</h4>');

        var text = '';
        for(var i=0; i<ps.length; i++){
            text += "<p>" + ps[i] + "</p>";
        }


        $('#title').fadeOut(500, function() {
            $(this).html('<h4>' + title + '</h4>').fadeIn(500);
        });
        $('#content').fadeOut(700, function() {
            $(this).html(text).fadeIn(700);
        });
        $('#content').scrollTop(0);
        //$("#content").html(text);
        $("#loc_name").html(data.location);
        $("#instance_id").val(instanceId);
        $("#u_count").html(user_label_count);
        $("#t_count").html(remaind_count);
    }
}
