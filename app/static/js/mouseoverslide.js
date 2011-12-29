
	$(document).ready(function(){
		//マスオーバー時にキャンプション表示
		$('.boxgrid.captionfull').hover(function(){
			$(".cover", this).stop().animate({top:'220px'},{queue:false,duration:160});
		}, function() {
			$(".cover", this).stop().animate({top:'350px'},{queue:false,duration:160});
		});
		//マウスオーバー時に残りを表示
		$('.boxgrid.caption').hover(function(){
			$(".cover", this).stop().animate({top:'100px'},{queue:false,duration:160});
		}, function() {
			$(".cover", this).stop().animate({top:'125px'},{queue:false,duration:160});
		});
		//マスオーバー時に右にスライド
		$('.boxgrid.slideright').hover(function(){
			$(".cover", this).stop().animate({left:'450px'},{queue:false,duration:300});
		}, function() {
			$(".cover", this).stop().animate({left:'0px'},{queue:false,duration:300});
		});	
		//マスオーバー時に右下にスライド
		$('.boxgrid.thecombo').hover(function(){
			$(".cover", this).stop().animate({top:'300px', left:'450px'},{queue:false,duration:300});
		}, function() {
			$(".cover", this).stop().animate({top:'0px', left:'0px'},{queue:false,duration:300});
		});
		//マスオーバー時に上にスライド
		$('.boxgrid.slidedown').hover(function(){
			$(".cover", this).stop().animate({top:'-300px'},{queue:false,duration:300});
		}, function() {
			$(".cover", this).stop().animate({top:'0px'},{queue:false,duration:300});
		});
		//マスオーバー時に他の画像も表示
		$('.boxgrid.peek').hover(function(){
			$(".cover", this).stop().animate({top:'90px'},{queue:false,duration:160});
		}, function() {
			$(".cover", this).stop().animate({top:'0px'},{queue:false,duration:160});
		});
	});