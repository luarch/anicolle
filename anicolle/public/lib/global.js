var eid = -1;
var bgmEditorTpl =
    '<div class="bgm-editor"><form><div class="row"><div class="one-half column"><label for="bgmName">番剧名称</label><input type="text" id="bgmName" class="u-full-width" value="{{bgmTitle}}"></div><div class="three columns"><label for="bgmCurEpi">已看到</label><input type="number" id="bgmCurEpi" class="u-full-width" value="{{bgmCurEpi}}"></div><div class="three columns"><label for="bgmOnAir">更新于</label><select id="bgmOnAir" class="u-full-width"><option value="1">周一</option><option value="2">周二</option><option value="3">周三</option><option value="4">周四</option><option value="5">周五</option><option value="6">周六</option><option value="7">周日</option><option value="9">不定期</option><option value="0">已完结</option></select></div></div><div class="row"><label for="bgmChkkey">更新检索关键词 (通过 漫游BT服务器)</label><input type="text" id="bgmChkkey" class="u-full-width" value="{{bgmChkKey}}"></div><a href="javascript:void(0)" class="button button-primary" onclick="doModify({{bgmBid}})">保存</a> <a href="javascript:void(0)" class="button" onclick="doRemove({{bgmBid}})">删除</a> <a href="javascript:void(0)" class="button" onclick="hideBgmEditor()">取消</a></form></div>';

var bgmRowTpl =
    '<div class="row bgm-row" style="margin-top: 50px" data-bid="{{bgmBid}}" data-onair="{{bgmOnAirCode}}"><div class="two-thirds column"><h3><small>[{{bgmOnAir}}]</small> <a href="javascript:void(0)" class="bgm-title">{{bgmTitle}} (<span class="cur-epi">{{bgmCurEpi}}</span>)</a></h3></div><div class="one-third column bgm-action"><a class="button button-primary" href="javascript:void(0)" onclick="doPlus({{bgmBid}})">+1</a> <a class="button" href="javascript:void(0)" onclick="doDecrease({{bgmBid}})">-1</a> <a class="button" href="javascript:void(0)" onclick="doChk({{bgmBid}})">检查</a></div></div>';

anicolle = {

    urls: {
        getAni: "/action/get/",
        modify: "/action/modify/",
        plus: "/action/plus/",
        decrease: "/action/decrease/",
        add: "/action/add",
        remove: "/action/remove/",
        chkup: "/action/chkup/"
    },

    getAni: function(bid){
        return $.ajax( {
            url: this.urls.getAni + bid,
            type: "GET",
            dataType: "json"
        });
    },

    plus: function( bid ) {
        return $.ajax({
            url: this.urls.plus + bid,
            type: "GET",
            dataType: "json"
        });
    },

    decrease: function( bid ) {
        return $.ajax({
            url: this.urls.decrease + bid,
            type: "GET",
            dataType: "json"
        });
    },

    modify: function( bid, name, cur_epi, on_air, chk_key ) {
        return $.ajax({
            url: this.urls.modify + bid,
            type: "POST",
            data: { "name": name, "cur_epi": cur_epi,
                    "on_air": on_air, "chk_key": chk_key }
        });
    },

    add: function( name, cur_epi, on_air, chk_key ) {
        return $.ajax({
            url: this.urls.add,
            type: "POST",
            data: { "name": name, "cur_epi": cur_epi,
                    "on_air": on_air, "chk_key": chk_key }
        });
    },

    remove: function( bid ) {
        return $.ajax({
            url: this.urls.remove + bid,
            type: "GET"
        });
    },

    chkup: function( bid ) {
        return $.ajax({
            url: this.urls.chkup + bid,
            type: "GET",
            dataType: "json"
        });
    }
};

function showBgmEditor(obj) {
    $(".bgm-editor").remove();
    var beh = bgmEditorTpl;
    if( $(obj).hasClass('bgm-row') ) {
        var r = anicolle.getAni( getBid(obj) );
        r.done(function(data){
            beh = beh.replace(/{{bgmBid}}/g, data[0]);
            beh = beh.replace(/{{bgmTitle}}/g, escapeQuote(data[1]));
            beh = beh.replace(/{{bgmCurEpi}}/g, data[2]);
            beh = beh.replace(/{{bgmChkKey}}/g, escapeQuote(data[4]));
            $(obj).append(beh);
            $(".bgm-editor select option[value="+data[3]+"]").attr("selected", true);
        });
    } else {
        beh = beh.replace(/{{bgmBid}}/g, 0);
        beh = beh.replace(/{{bgmTitle}}/g, "");
        beh = beh.replace(/{{bgmCurEpi}}/g, "");
        beh = beh.replace(/{{bgmChkKey}}/g, "");
        $(obj).append(beh);
        $(".bgm-editor select option[value=0]").attr("selected", true);
        $(".bgm-editor a.button:eq(1)").remove();
    }
}

function hideBgmEditor() {
    $('.bgm-editor').remove();
}

function genBgmRow( row ) {
    var brh = bgmRowTpl;
    brh = brh.replace(/{{bgmBid}}/g, row['id']);
    brh = brh.replace(/{{bgmTitle}}/g, escapeQuote(row['name']));
    brh = brh.replace(/{{bgmCurEpi}}/g, row['cur_epi']);
    var onAirDict = [ '结', '一', '二', '三', '四', '五', '六', '日' ];
    var onAir = onAirDict[row['on_air_day']];
    brh = brh.replace(/{{bgmOnAir}}/g, onAir);
    brh = brh.replace(/{{bgmOnAirCode}}/g, row['on_air_day']);
    return brh;
}

function showBgm() {
    $('.row.bgm-row').remove();
    $(".action-row input").val("");

    var bgmRowH = "";

    var r = anicolle.getAni('');
    r.done( function(data){
        data.forEach( function(row){
            bgmRowH += genBgmRow(row);
        });
        $('.row.action-row').after(bgmRowH);
        $('.bgm-title').click(function(){
            bgmO = $(this).parents(".row");
            showBgmEditor(bgmO);
        });
    });
}

function doPlus(bid) {
    var r = anicolle.plus( bid );
    var curEpi = $( getObjByBid(bid) ).find( ".cur-epi" ).text();
    curEpi  = parseFloat(curEpi);
    curEpi += 1;

    $( getObjByBid(bid) ).find(".cur-epi")
    .animate({opacity: 0})
    .text(curEpi)
    .animate({opacity: 1});
}

function doDecrease(bid) {
    var r = anicolle.decrease( bid );
    var curEpi = $( getObjByBid(bid) ).find( ".cur-epi" ).text();
    curEpi  = parseFloat(curEpi);
    curEpi -= 1;

    $( getObjByBid(bid) ).find(".cur-epi")
    .animate({opacity: 0})
    .text(curEpi)
    .animate({opacity: 1});
}

function doModify(bid) {
    if(!bid) {
        doAdd();
        return;
    }
    var r = anicolle.modify( bid, $("#bgmName").val(), $("#bgmCurEpi").val(), $("#bgmOnAir").val(), $("#bgmChkkey").val() );
    r.done(function(){
        hideBgmEditor();
        showBgm();
    });
}

function doAdd() {
    var r = anicolle.add( $("#bgmName").val(), $("#bgmCurEpi").val(), $("#bgmOnAir").val(), $("#bgmChkkey").val() );
    r.done(function(){
        hideBgmEditor();
        showBgm();
    });
}

function doRemove(bid) {
    if( confirm("你确定要删除这个番剧吗？" ) ) {
        var r = anicolle.remove( bid );
        r.done(function(){
            showBgm();
        });
    }
}

function doChk(bid) {
    obj = getObjByBid(bid);
    obj = $(obj).find('.button:eq(2)');
    $(obj).text("检查中...");
    var r = anicolle.chkup( bid );
    r.done(function(data){
        $(obj).text("检查");
        if( data ) {
            prompt("找到更新 " + data.magname, data.maglink);
        } else {
            alert("未发现更新");
        }
    });
}

function initSearch() {
    $(".action-row input").keyup(function(){
        var key = $(this).val();
        if(key) {
            if( key.match(/^w\d$/) ) {
                key = key.replace("w", "");
                $('.bgm-row').stop().fadeOut(function(){
                    $('.bgm-row[data-onair='+key+']').stop().fadeIn();
                });
            } else {
                $('.bgm-row').each(function(){
                    var title = $(this).find('.bgm-title').text();
                    var re = new RegExp(".*"+key+".*", "gi");
                    if( !re.test(title) ){
                        $(this).stop().fadeOut();
                    } else {
                        $(this).stop().fadeIn();
                    }
                });
            }
        } else {
            $('.bgm-row').stop().fadeIn();
        }
    });
}

$(document).ready(function(){
    showBgm();
    initSearch();
});

function escapeQuote(str) {
    return str.replace( /"/g, "&quot;" );
}

function getBid(obj) {
    return $(obj).attr("data-bid");
}

function getObjByBid(bid) {
    return $('.bgm-row[data-bid=' + bid + ']');
}
