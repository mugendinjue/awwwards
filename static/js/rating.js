$(document).ready(function(){
  $('#btnShow,#submit').click(function(){
    $('#rating').slideToggle('slow')
  })
  var project = $(this).find($('.projectId'))
  $('form#rateForm').submit(function(e){
    e.preventDefault()
    rateForm = $('form#rateForm')
    $.ajax({
      'url':'/rating/data/'+project.val()+'',
      'type':'POST',
      'data':rateForm.serialize(),
      'dataType':'json',
      'success':function(data){
        console.log(data['success'])
      },
    })
    $('#id_design').val('')
    $('#id_usability').val('') 
    $('#id_creativity').val('')
    $('#id_content').val('') 
  })
})

