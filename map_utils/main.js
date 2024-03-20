// SVGを表示する関数
function displaySVG(svgData) {
    const svgContainer = document.getElementById('svgContainer');
    svgContainer.innerHTML = svgData;
  }
  
  // ファイルが選択されたときの処理
  document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
  
    reader.onload = function(event) {
      const svgData = event.target.result;
      displaySVG(svgData);
    };
  
    reader.readAsText(file);
  });
  
  let selectedArea = null;
  
  // ユーザーが選択した範囲を表示する関数
  function updateSelectedArea(x, y, width, height) {
    // 以前の選択範囲があれば削除する
    if (selectedArea) {
      selectedArea.remove();
    }
  
    selectedArea = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    selectedArea.setAttribute("x", x);
    selectedArea.setAttribute("y", y);
    selectedArea.setAttribute("width", width);
    selectedArea.setAttribute("height", height);
    selectedArea.setAttribute("stroke", "red");
    selectedArea.setAttribute("stroke-width", "2");
    selectedArea.setAttribute("fill", "none");
  
    const svgElement = document.querySelector('svg');
    svgElement.appendChild(selectedArea);
  
    // ViewBoxを更新して表示
    const viewBoxDisplay = document.getElementById('viewBoxDisplay');
    viewBoxDisplay.textContent = `ViewBox: ${x} ${y} ${width} ${height}`;
  }
  
  // マウスイベントリスナーを追加して選択範囲を更新
  document.getElementById('svgContainer').addEventListener('mousedown', function(event) {
    const svgContainer = document.getElementById('svgContainer');
    const svgRect = svgContainer.getBoundingClientRect();
    
    const startX = event.clientX - svgRect.left;
    const startY = event.clientY - svgRect.top;
  
    let selectedAreaWidth = 0;
    let selectedAreaHeight = 0;
  
    function updateSelection(event) {
      selectedAreaWidth = event.clientX - svgRect.left - startX;
      selectedAreaHeight = event.clientY - svgRect.top - startY;
  
      updateSelectedArea(startX, startY, selectedAreaWidth, selectedAreaHeight);
    }
  
    function endSelection() {
      document.removeEventListener('mousemove', updateSelection);
      document.removeEventListener('mouseup', endSelection);
    }
  
    document.addEventListener('mousemove', updateSelection);
    document.addEventListener('mouseup', endSelection);
  });
  