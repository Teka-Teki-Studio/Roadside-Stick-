const path = require('path');
const fs = require('fs');
const libGD = require('./libGD.js');

const PROJECT_PATH = path.resolve(__dirname, '..', '..', 'game.json');

libGD().then(gd => {
  console.log('libGD loaded successfully! Version:', gd.VersionWrapper.fullString());
  const jsonContent = fs.readFileSync(PROJECT_PATH, 'utf8');
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const serializer = gd.Serializer;
  const projectElement = serializer.fromJSON(jsonContent);
  project.unserializeFrom(projectElement);
  projectElement.delete();

  const layoutCount = project.getLayoutsCount();
  console.log(`Project loaded. Total layouts: ${layoutCount}`);

  for (let lIdx = 0; lIdx < layoutCount; lIdx++) {
    const layout = project.getLayoutAt(lIdx);
    const layoutName = layout.getName();
    const gen = new gd.LayoutCodeGenerator(project);
    const includes = new gd.SetString();
    const diag = new gd.DiagnosticReport();
    
    const code = gen.generateLayoutCompleteCode(layout, includes, diag, false);
    console.log(`Layout '${layoutName}' compiled: ${code.length} chars, diags: ${diag.count()}`);
  }

  project.delete();
  console.log('ALL COMPILED SUCCESSFULLY!');
}).catch(err => {
  console.error('libGD error:', err);
});
