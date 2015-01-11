var queue = {refresh:true}
queue.tdiff = function(d1, d2){
    d2=typeof a !== 'undefined' ? d2 : new Date();
    var diff = d2-d1;
    var ret = {allmillis: diff};
    diff=Math.floor(diff/1000);
    ret.secs=diff%60;

    diff=Math.floor(diff/60);
    ret.mins=diff%60;

    diff=Math.floor(diff/60);
    ret.hrs=diff;

    ret.tparse=ret.hrs+":"+(ret.mins<10?"0"+ret.mins:ret.mins)
    return ret;
}

queue.ar = $('#ar');
queue.usrs = $('.usr');

queue.usrs.each( // Let the client parse the time elapsed
    function(i){
	var c=$(this).children();
	var p=$(c[0]).text().replace(/-/g,' ').replace(/:/g,' ').split(' ');
	var d=new Date(p[0],p[1]-1,p[2],p[3],p[4],p[5],0);
	$(c[1]).text(queue.tdiff(d).tparse);
    }
);

queue.usrs.click( function(d,h){
    if (queue.ar.prop('checked')){ // if autoreload is checked, uncheck it
        queue.ar.click();
    }

    var id = $(this).attr('id');
    document.forms[0]['hash'].value=id;
    $('.frmhidden').slideDown();
    $('.usr').each(function(){
        if ($(this).attr('id')!==id){
            $(this) // snippet from http://stackoverflow.com/a/3410943
                .find('td')
                .wrapInner('<div style="display: block;" />')
                .parent()
                .find('td > div')
                .slideUp(700, function () {
                    $(this).parent().parent().remove();
            });
        }
    });
});

queue.validate = function(){
    var pn = document.forms[0]['phone'].value;
    var c = document.forms[0]['carrier'].value;
    console.log(pn);
    console.log(c);
    var carr = ['v','a','s','t','vm'];
    if (isNaN(pn) || pn.length!=10) {
        alert("Please input a valid phone number");
        document.forms[0]['phone'].value="";
        document.getElementsByName('phone')[0].focus();
        return false;
    }
    if (carr.indexOf(c)==-1){
        alert('Please select a carrier');
        document.getElementsByName('carrier')[0].focus();
        return false;
    }
    return true;
}

queue.rsttmr = function(){ // reset timer
    queue.t = setTimeout(function(){
        if (queue.ar.prop('checked')){
            // alert('refresh');
            window.location.reload()
        }
    },20000);
};
queue.rsttmr()
