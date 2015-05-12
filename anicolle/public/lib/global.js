var eid = -1;
var bgmEditorTpl = 
    '<div class="bgm-editor"><form><div class="row"><div class="one-half column"><label for="bgmName">番剧名称</label><input type="text" id="bgmName" class="u-full-width" value="{{bgmTitle}}"></div><div class="three columns"><label for="bgmCurEpi">已看到</label><input type="number" id="bgmCurEpi" class="u-full-width" value="{{bgmCurEpi}}"></div><div class="three columns"><label for="bgmOnAir">更新于</label><select id="bgmOnAir" class="u-full-width"><option value="1">周一</option><option value="2">周二</option><option value="3">周三</option><option value="4">周四</option><option value="5">周五</option><option value="6">周六</option><option value="7">周日</option><option value="9">不定期</option><option value="0">已完结</option></select></div></div><div class="row"><label for="bgmChkkey">更新检索关键词</label><input type="text" id="bgmChkkey" class="u-full-width" value="{{bgmChkKey}}"></div><a href="javascript:void(0)" class="button button-primary">保存</a> <a href="javascript:void(0)" class="button" onclick="hideBgmEditor()">取消</a></form></div>';

var bgmRowTpl = 
    '<div class="row bgm-row" style="margin-top: 50px" data-bid="{{bgmBid}}"><div class="two-thirds column"><h3><small>[{{bgmOnAir}}]</small> <a href="javascript:void(0)" class="bgm-title">{{bgmTitle}} (<span class="cur-epi">{{bgmCurEpi}}</span>)</a></h3></div><div class="one-third column bgm-action"><a class="button button-primary" href="javascript:void(0)" onclick="doPlus({{bgmBid}})">+1</a> <a class="button" href="javascript:void(0)" onclick="doDecrease({{bgmBid}})">-1</a> <a class="button" href="javascript:void(0)" onclick="doChk({{bgmBid}})">检查</a></div></div>';

anicolle = {

    urls: {
        getAni: "/action/get/",
        modify: "/action/modify/",
        plus: "/action/plus/",
        decrease: "/action/decrease/",
        add: "/action/add/",
        remove: "/action/remove/"
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
    }

};

function showBgmEditor(obj) {
    $(".bgm-editor").remove();
    var beh = bgmEditorTpl;
    var r = anicolle.getAni( getBid(obj) );
    r.done(function(data){
        beh = beh.replace(/{{bgmTitle}}/g, escapeQuote(data[1]));
        beh = beh.replace(/{{bgmCurEpi}}/g, data[2]);
        beh = beh.replace(/{{bgmChkKey}}/g, escapeQuote(data[4]));
        $(obj).append(beh);
        $(".bgm-editor select option[value="+data[3]+"]").attr("selected", true);
    });
}

function hideBgmEditor() {
    $('.bgm-editor').remove();
}

function genBgmRow( row ) {
    var brh = bgmRowTpl;
    brh = brh.replace(/{{bgmBid}}/g, row[0]);
    brh = brh.replace(/{{bgmTitle}}/g, escapeQuote(row[1]));
    brh = brh.replace(/{{bgmCurEpi}}/g, row[2]);
    var onAirDict = [ '结', '一', '二', '三', '四', '五', '六', '日' ];
    var onAir = onAirDict[row[3]];
    brh = brh.replace(/{{bgmOnAir}}/g, onAir);
    return brh;
}

function showBgm() {
    $('.row.bgm-row').remove();

    var bgmRowH = "";

    var r = anicolle.getAni('');
    r.done( function(data){
        data.forEach( function(row){
            bgmRowH += genBgmRow(row);
        });
        $('.row.action-row').after(bgmRowH);
        $('.bgm-row .bgm-title').click(function(){
            bgmO = $(this).parents(".bgm-row");
            showBgmEditor(bgmO);
        });
    });
}

function doPlus(bid) {
    // var r = anicolle.plus( bid );
    var curEpi = $( getObjByBid(bid) ).find( ".cur-epi" ).text();
    curEpi  = parseFloat(curEpi);
    curEpi += 1;

    $( getObjByBid(bid) ).find(".cur-epi")
    .animate({opacity: 0})
    .text(curEpi)
    .animate({opacity: 1});
}

function doDecrease(bid) {
    // var r = anicolle.decrease( bid );
    var curEpi = $( getObjByBid(bid) ).find( ".cur-epi" ).text();
    curEpi  = parseFloat(curEpi);
    curEpi -= 1;

    $( getObjByBid(bid) ).find(".cur-epi")
    .animate({opacity: 0})
    .text(curEpi)
    .animate({opacity: 1});
}


$(document).ready(function(){

    showBgm();

});

function escapeQuote( str ) {
    return str.replace( /"/g, "&quot;" );
}

function getBid( obj ) {
    return $(obj).attr("data-bid");
}

function getObjByBid( bid ) {
    return $('.bgm-row[data-bid=' + bid + ']');
}
