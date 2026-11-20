const libGD = require('C:\\Users\\ASUS\\.gemini\\antigravity\\brain\\29446708-9512-473e-8ad5-01a604faa9f5\\scratch\\libGD_extracted.js');
const fs = require('fs');

libGD().then(gd => {
  const jsonContent = fs.readFileSync('StickScavenger.json', 'utf8');
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const serializer = gd.Serializer;
  const projectElement = serializer.fromJSON(jsonContent);
  project.unserializeFrom(projectElement);
  projectElement.delete();

  const layout = project.getLayoutAt(0);
  console.log('Layout name:', layout.getName());

  const gen = new gd.LayoutCodeGenerator(project);
  const includes = new gd.SetString();
  const diag = new gd.DiagnosticReport();
  const code = gen.generateLayoutCompleteCode(layout, includes, diag, false);
  console.log('SUCCESS! Generated JS code length:', code.length);
  fs.writeFileSync('title_screen_compiled.js', code);
  console.log('Saved title_screen_compiled.js');

  const lines = code.split('\n');
  console.log('Total JS lines in compiled code:', lines.length);

  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.includes('isMouseButtonPressed') || l.includes('isKeyPressed') || l.includes('fade_state') || l.includes('replaceScene')) {
      const start = Math.max(0, i - 4);
      const end = Math.min(lines.length - 1, i + 14);
      console.log(`\n=== Line ${i}: ${l.trim()} ===`);
      for (let j = start; j <= end; j++) {
        console.log(`${j}: ${lines[j]}`);
      }
      i = end;
    }
  }
}).catch(err => {
  console.error('libGD Compilation Error:', err);
});
