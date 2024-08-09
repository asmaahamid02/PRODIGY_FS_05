$(document).ready(function () {
  const sidebar = $('#main-sidebar')
  const sidebarToggler = $('.sidebar-toggler')

  $(document)
    .on('click', '.sidebar-toggler', function (e) {
      e.preventDefault()
      console.log('clicked')
      sidebar.toggleClass('-translate-x-full')
    })
    .on('click', function (e) {
      if (
        !sidebar.is(e.target) &&
        sidebar.has(e.target).length === 0 &&
        !sidebarToggler.is(e.target) &&
        sidebarToggler.has(e.target).length === 0 &&
        !sidebar.hasClass('-translate-x-full')
      ) {
        sidebar.addClass('-translate-x-full')
      }
    })
})
