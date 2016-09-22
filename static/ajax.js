$(document).ready(function(){
	console.log($('#currentPage').val());
	$('select').change(function(){		
		var id = $(this).attr('id');
		var value = $(this).val();
		var parent = $(this).parent();
		var divParent = parent.parent();

		$.post(
		{
			url: '/ajax/' + id + '/' + value,
			success: function(html){												
				divParent.attr('class', 'container ' + value);				

			}
		}
		);

	});

	$('#next').click(function(e){
		e.preventDefault();

		var next = $(this).attr('href');
		$.post(
			{
				url: '/ajax/insert/' + $('#currentPage').val(),
				data: $('form').serialize(),
				success: function(html){
					 // $('html').html(html);
					console.log("next: ", next);
					window.location = next;
				}
			}
		);
	});
});