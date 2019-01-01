<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>From RE to DFA</title>
  <script src="js/d3.v4.min.js" charset="utf-8"></script>
  <script src="js/dagre-d3.min.js"></script>
  <script src="js/jquery.min.js"></script>
  <script type="text/javascript" src="js/graph.js"></script>
  <link rel="stylesheet" type="text/css" href="css/style.css">
</head>
<body>
<div class="form">
  <input type="text" class="value" id="string">
  <input type="button" onclick="Ajax()" class="button" value="Build">
  <input type="text" class="value" id="target">
  <input type="button" onclick="judge()" class="button" value="Judge">
</div>
<div class="set" id="set">
</div>
<div class="title">NFA</div>
<div class="title">DFA</div>
<div class="NFA" id="NFA">
  <svg id="svg1" width="550" height="400"></svg>
</div>

<div class="DFA" id="DFA">
  <svg id="svg2" width="550" height="400"></svg>
</div>

</body>
</html>