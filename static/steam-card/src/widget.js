(function(d) {
  var base = "//cdn.igiari.moe";
  var i, count = 0;

  function queryclass(name) {
    if (d.querySelectorAll) {
      return d.querySelectorAll('.' + name);
    }
    var elements = d.getElementsByTagName('div');
    var ret = [];
    for (i = 0; i < elements.length; i++) {
      if (~elements[i].className.split(' ').indexOf(name)) {
        ret.push(elements[i]);
      }
    }
    return ret;
  }

  function querydata(element, name) {
    return element.getAttribute('data-' + name);
  }

  function heighty(iframe) {
    if (window.addEventListener) {
      window.addEventListener('message', function(e) {
        if (iframe.id === e.data.sender) {
          iframe.height = e.data.height;
        }
      }, false);
    }
  }

  function render(card) {
    var cardurl = base + '/steamCard';
    var id = querydata(card, 'id');
    if (!id) {
      return;
    }

    count += 1;

    var lang = querydata(card, 'lang') || 'zh';
    var width = querydata(card, 'width') || 280;
    var identity = 'stcard-' + id + '-' + count;

    var iframe = d.createElement('iframe');
    iframe.setAttribute('id', identity);
    iframe.setAttribute('frameborder', 0);
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('allowtransparency', true);


    var url = cardurl + '?id=' + id + '&identity=' + identity + '&lang=' + lang + '&width=' + width;
    iframe.src = url;
    iframe.width = width || Math.min(card.parentNode.clientWidth || 280, 280);
    
    heighty(iframe);
    card.parentNode.replaceChild(iframe, card);
    return iframe;
  }

  var cards = queryclass('steam-card');
  for (i = 0; i < cards.length; i++) {
    render(cards[i]);
  }
})(document);
