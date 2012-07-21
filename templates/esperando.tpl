<html>
% if user_status["logged_in"]:
	% if user_status["current_user"].nombre in esperando:
     	<head><meta http-equiv="refresh" content="5"></head>
	% elif user_status["current_user"].nombre in partidas:
		% partida_id = partidas[user_status["current_user"].nombre][-1]
	     <body><script type="text/javascript">parent.document.location =
"{{base_url}}/jugar/{{partida_id}}"</script></body>
	% end
% end
</html>
