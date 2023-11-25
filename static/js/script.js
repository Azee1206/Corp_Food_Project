$(function () {
  $('[data-toggle="popover"]').popover()
})
function selectCardF(card) {
      var cards = document.getElementsByClassName("f");
      for (var i = 0; i < cards.length; i++) {
        cards[i].classList.remove("selected");
      }
      card.classList.add("selected");
}
function selectCardS(card) {
      var cards = document.getElementsByClassName("s");
      for (var i = 0; i < cards.length; i++) {
        cards[i].classList.remove("selected");
      }
      card.classList.add("selected");
}
function selectCardSL(card) {
      var cards = document.getElementsByClassName("sl");
      for (var i = 0; i < cards.length; i++) {
        cards[i].classList.remove("selected");
      }
      card.classList.add("selected");
}
function selectCardd(card) {
      var cards = document.getElementsByClassName("d");
      for (var i = 0; i < cards.length; i++) {
        cards[i].classList.remove("selected");
      }
      card.classList.add("selected");
}
