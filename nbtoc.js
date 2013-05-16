// adapted from https://gist.github.com/magican/5574556

function clone_anchor(h){
  // clone link
  var a = $(h).find('a').clone();
  a.attr('href', '#' + a.attr('id'));
  a.attr('id', '');
  return a;
}

function lvl(header){
  if (header !== undefined)
  return $(header).prop('tagName').toLowerCase().substring(1);
  else return 0;
}

function table_of_contents(){
  var headers = $('h1, h2, h3, h4');
  var ol = $("<ol/>").addClass("nested");
  $("#toc").empty().append(ol);
  
  $.each(headers, function(i, h) {
    console.log(i, h);
    ol.append(
      $("<li/>").addClass("nested").append(clone_anchor(h))
    );
    
    if ( lvl(h) < lvl(headers[i+1]) ) {
      var new_ol = $("<ol/>").addClass("nested");
      ol.append(new_ol);
      ol = new_ol;
    } else if ( lvl(h) > lvl(headers[i+1]) ) {
      ol = $("<ol/>").addClass("nested");
      $("#toc").append(ol);
    }
  });

  $('#toc-wrapper .header').click(function(){
    $('#toc').slideToggle();
    $('#toc-wrapper').toggleClass('closed');
    if ($('#toc-wrapper').hasClass('closed')){
      $('#toc-wrapper .hide-btn').text('[show]');
    } else {
      $('#toc-wrapper .hide-btn').text('[hide]');
    }
    return false;
  })

  $(window).resize(function(){
    $('#toc').css({maxHeight: $(window).height() - 200})
  })

  $(window).trigger('resize')
}

table_of_contents();


