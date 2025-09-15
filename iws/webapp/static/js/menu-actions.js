function openSideNavbar() {
    var sideNavBarElement = document.getElementById("sideNavBarDiv");
    if (sideNavBarElement) {
        sideNavBarElement.style.width = "250px";
    }
}

/* Set the width of the side navigation to 0 */
function closeSideNavbar() {
    var sideNavBarElement = document.getElementById("sideNavBarDiv");
    if (sideNavBarElement) {
        sideNavBarElement.style.width = "0";
    }
}

/**
 * Init Menu
 */
function initMenu() {
    // alert("document loaded! Init menu")

    /**
     * Add click event to active menu item
     */
    $("li").click(function (event) {
        // event.preventDefault();
        // console.log(event);

        // alert("clicked on menu item: " + this.innerHTML);
        // iterate each element and toggle active class
        $("li").each(function (index, element) {
            // console.log(index + ": " + $(this).text());
            // console.log(element);
            if ($(this).hasClass("active")) {
                $(this).toggleClass("active");
            }
        });

        // toggleClass() switches the active class 
        // $("li").toggleClass("active");
        // $("li").addClass("active");
        $(this).addClass("active");

        // stop executing current event
        if ($(this).text() == 'Dropdown') {
            event.preventDefault();
        }
    });

}

/**
 * On document ready
 */
$(document).ready(function () {
    //    console.log($(this).text());
    initMenu();
});
