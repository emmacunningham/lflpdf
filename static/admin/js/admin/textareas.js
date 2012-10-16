tinyMCE.init({
  mode : "textareas",
  theme : "advanced",
  theme_advanced_toolbar_location : "top",
  theme_advanced_toolbar_align : "left",
  theme_advanced_buttons1 : "bold,italic,underline,separator,bullist,outdent,indent,separator,undo,redo,separator",
  theme_advanced_buttons2 : "table,separator,row_after,row_before,separator,delete_row,delete_table",
  theme_advanced_buttons3 : "removeformat",
  plugins: "table, paste", 
  paste_remove_styles: true,
  paste_remove_spans: true,
  table_col_limit : 2,
  plugin_insertdate_dateFormat : "%m/%d/%Y",
  plugin_insertdate_timeFormat : "%H:%M:%S",
  extended_valid_elements : "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
  fullscreen_settings : {
    theme_advanced_path_location : "top",
    theme_advanced_buttons1 : "fullscreen,separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
    theme_advanced_buttons2 : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
    theme_advanced_buttons3 : "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
  }
});