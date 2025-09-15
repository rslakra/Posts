/**
 * On document ready
 */
//$(document).ready(function () {
//    console.log($(this).text());
////    alert("document loaded!")
//});

/**
 * Add Event Listener
 */
//window.addEventListener("load", (event) => {
//    console.log("page is fully loaded");
//});

/**
 * Add Slide Show Contents in HTML Page

<!-- Slide Show -->
<section>
  <img class="divSlidesCarousel" src="img_band_la.jpg" style="width:100%"/>
  <img class="divSlidesCarousel" src="img_band_ny.jpg" style="width:100%"/>
  <img class="divSlidesCarousel" src="img_band_chicago.jpg" style="width:100%"/>
</section>

 */

var slideIndex = 0;
showCarousel();

function showCarousel() {
  var index;
  var divSlidesCarousel = document.getElementsByClassName("divSlidesCarousel");
  for (index = 0; index < divSlidesCarousel.length; index++) {
    divSlidesCarousel[index].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > divSlidesCarousel.length) {slideIndex = 1}
  divSlidesCarousel[slideIndex-1].style.display = "block";
  setTimeout(showCarousel, 3000);
}