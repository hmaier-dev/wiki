num=$( cat content/*.md | wc -l )

echo "
<footer class=index_footer>

This wiki is generated from $num lines of markdown.

</footer>
" >> layouts/partials/index_footer.html
