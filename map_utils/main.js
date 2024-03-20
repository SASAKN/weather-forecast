document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
      const svgData = e.target.result;
      const svgContainer = document.getElementById('svg-container');
      svgContainer.innerHTML = svgData;
    };
    reader.readAsText(file);
  });