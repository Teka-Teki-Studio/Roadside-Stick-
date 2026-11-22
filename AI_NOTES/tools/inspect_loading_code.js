const path = require('path');
const fs = require('fs');
const libGD = require('./libGD.js');

const PROJECT_PATH = path.resolve(__dirname, '..', '..', 'game.json');

libGD().then(gd => {
  const jsonContent = fs.readFileSync(PROJECT_PATH, 'utf8');
  const project = new gd.ProjectHelper.createNewGDJSProject();
  const serializer = gd.Serializer;
  const projectElement = serializer.fromJSON(jsonContent);
  project.unserializeFrom(projectElement);
  projectElement.delete();

  const layout = project.getLayout('Loading');
  const gen = new gd.LayoutCodeGenerator(project);
  const includes = new gd.SetString();
  const diag = new gd.DiagnosticReport();
  
  const code = gen.generateLayoutCompleteCode(layout, includes, diag, false);
  console.log("=== COMPILED LOADING CODE ===");
  console.log(code);

  project.delete();
});
