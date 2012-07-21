<html><body>
<script type="text/javascript">
var turno = {{ turno_jugador }};
function reloading() {
	document.location.reload();
}
if (turno != parent.turno) {
	parent.document.location.reload();
} else {
	setTimeout(reloading, 2000);
}
</script>
</body></html>
