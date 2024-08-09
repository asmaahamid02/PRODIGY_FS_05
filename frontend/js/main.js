$.ajaxSetup({
  beforeSend: function beforeSend(xhr, settings) {
    function getCookie(name) {
      let cookieValue = null

      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')

        for (let i = 0; i < cookies.length; i += 1) {
          const cookie = jQuery.trim(cookies[i])

          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === `${name}=`) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }

      return cookieValue
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    }
  },
})

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
    .on('click', '.modal-toggler', function (e) {
      e.preventDefault()
      console.log('clicked')
      toggle_modal($(this).data('modal-toggle'))
    })
    .on('change', '#post-image', function (e) {
      const file = $(this)[0].files[0]
      const reader = new FileReader()

      reader.onload = function (readerEvent) {
        $('#post-image-preview').attr('src', readerEvent.target.result)
      }

      reader.readAsDataURL(file)
    })
    .on('submit', '#post-form', function (e) {
      e.preventDefault()

      const data = new FormData($(this)[0])

      $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data,
        processData: false,
        contentType: false,
        success: (htmlData) => {
          toggle_message('close') //error message
          toggle_message('open', '', 'success')

          setTimeout(() => {
            toggle_message('close', '', 'success')
            reset_form()
            toggle_modal()

            $('.posts-container').prepend(htmlData)
          }, 1000)
        },
        error: (error) => {
          console.error('Post Form Error:', error)
          toggle_message('open', error.responseJSON.errors[0])
        },
      })
    })
})

function toggle_message(action = 'open', message = '', type = 'error') {
  const $selector =
    type === 'error' ? $('.post-error-message') : $('.post-success-message')

  if (type === 'error') {
    $selector.text(message)
  }

  if (action === 'open') {
    $selector.removeClass('hidden')
  } else {
    $selector.addClass('hidden')
  }
}

function reset_form() {
  $('#post-body').val('')
  $('#post-image').val('')
  $('#post-image-preview').attr('src', $('#post-image-preview').data('default'))
}

function toggle_modal(selector = 'new-post-modal') {
  $(`#${selector}`).toggleClass('hidden flex')
}
