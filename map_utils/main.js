// SVGを表示する関数
function displaySVG(svgData) {
    const svgContainer = document.getElementById('svgContainer');
    svgContainer.innerHTML = svgData;
  
    // ViewBoxを取得して表示
    updateViewBoxDisplay();
  }
  
  // ViewBoxを更新して表示する関数
// ViewBoxを更新して表示する関数
function updateViewBoxDisplay() {
    const svgElement = document.querySelector('svg');
    const viewBox = svgElement.getAttribute('viewBox');
    const [x, y, width, height] = viewBox.split(' ');
    const viewBoxDisplay = document.getElementById('viewBoxDisplay');
    viewBoxDisplay.textContent = `ViewBox: ${parseFloat(x)} ${parseFloat(y)} ${parseFloat(width)} ${parseFloat(height)}`;
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
  }
  
  // マウスイベントリスナーを追加して選択範囲を更新
  document.getElementById('svgContainer').addEventListener('mousedown', function(event) {
    const svgContainer = document.getElementById('svgContainer');
    const svgRect = svgContainer.getBoundingClientRect();
    const svgElement = document.querySelector('svg');
  
    const viewBox = svgElement.getAttribute('viewBox');
    const [vx, vy, vWidth, vHeight] = viewBox.split(' ');
  
    const clientX = event.clientX - svgRect.left;
    const clientY = event.clientY - svgRect.top;
  
    const svgWidth = svgElement.width.baseVal.value;
    const svgHeight = svgElement.height.baseVal.value;
  
    const scaleX = svgWidth / vWidth;
    const scaleY = svgHeight / vHeight;

    console.log(svgWidth, svgHeight, clientX, clientY, scaleX, scaleY)
  
    const x = (clientX - parseFloat(vx)) * scaleX;
    const y = (clientY - parseFloat(vy)) * scaleY;
  
    let selectedAreaWidth = 0;
    let selectedAreaHeight = 0;
  
    function updateSelection(event) {
      const clientWidth = event.clientX - svgRect.left;
      const clientHeight = event.clientY - svgRect.top;
  
      selectedAreaWidth = (clientWidth - clientX) * scaleX;
      selectedAreaHeight = (clientHeight - clientY) * scaleY;
  
      updateSelectedArea(x, y, selectedAreaWidth, selectedAreaHeight);
    }
  
    function endSelection() {
      document.removeEventListener('mousemove', updateSelection);
      document.removeEventListener('mouseup', endSelection);
    }
  
    document.addEventListener('mousemove', updateSelection);
    document.addEventListener('mouseup', endSelection);
  });
  