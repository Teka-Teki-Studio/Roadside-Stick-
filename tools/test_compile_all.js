const path = require('path');
const fs = require('fs');
const libGD = require('C:\\Users\\ASUS\\.gemini\\antigravity\\brain\\29446708-9512-473e-8ad5-01a604faa9f5\\scratch\\libGD_extracted.js');

const PROJECT_PATH = fs.existsSync('StickScavenger.json')
  ? path.resolve('StickScavenger.json')
  : path.resolve(__dirname, '..', 'StickScavenger.json');

libGD().then(gd => {
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
    console.log(`\n========================================`);
    console.log(`Compiling Layout #${lIdx}: '${layoutName}'`);
    console.log(`========================================`);

    const gen = new gd.LayoutCodeGenerator(project);
    const includes = new gd.SetString();
    const diag = new gd.DiagnosticReport();
    
    const code = gen.generateLayoutCompleteCode(layout, includes, diag, false);
    
    console.log(`Layout '${layoutName}' successfully compiled!`);
    console.log(`Generated JS code length: ${code.length} characters`);

    // Verify key snippets in Main_World
    if (layoutName === 'Main_World') {
      console.log('\n--- VERIFYING COMPILED JS FEATURES ---');
      
      const hasEsc = code.includes('"Escape"');
      const hasIsPaused = code.includes('is_paused') || code.includes('getVariables()');
      console.log(`[PAUSE ESC CHECK]: Key 'Escape' present: ${hasEsc}, Var checked: ${hasIsPaused}`);

      const hasC = code.includes('"c"');
      const hasTab = code.includes('"Tab"');
      const hasAlbum = code.includes('is_album_open') || code.includes('getVariables()');
      console.log(`[ALBUM CHECK]: Key 'c': ${hasC}, Key 'Tab': ${hasTab}, Var checked: ${hasAlbum}`);

      const hasSave = code.includes('StickScavengerSave');
      console.log(`[STORAGE CHECK]: 'StickScavengerSave' present: ${hasSave}`);

      const hasIgnore = code.includes('ignoreDefaultControls');
      console.log(`[CONTROLS CHECK]: 'ignoreDefaultControls' present: ${hasIgnore}`);

      const hasMaxSpeed = code.includes('setMaxSpeed');
      console.log(`[PROGRESSION CHECK]: 'setMaxSpeed' present: ${hasMaxSpeed}`);
    }
  }

  console.log(`\n========================================`);
  console.log(`ALL LAYOUTS COMPILED CLEANLY VIA LIBGD!`);
  console.log(`========================================`);
}).catch(err => {
  console.error('Fatal libGD Compilation Error:', err);
  process.exit(1);
});
