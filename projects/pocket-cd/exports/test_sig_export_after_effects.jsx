// =========================================================================
// Pocket Creator Director - After Effects ExtendScript (.jsx)
// Generated for Style DNA: Test Signature Reel
// Specifications: 1080x1920 @ 60fps, 9:16 Vertical Reel
// =========================================================================

(function createPocketCDComp() {
    app.beginUndoGroup("Pocket Creator Director - Test Signature Reel");

    var project = app.project;
    if (!project) {
        project = app.newProject();
    }
    project.bitsPerChannel = 16;

    // 1. Create Master 9:16 Vertical Composition
    var compName = "Test Signature Reel - Timeline";
    var comp = project.items.addComp(compName, 1080, 1920, 1.0, 22.0, 60);
    comp.motionBlur = true;
    comp.bgColor = [0.07, 0.08, 0.10];

    // 2. Flash Open (White Strobe Stomp)
    var flashSolid = comp.layers.addSolid([1.0, 1.0, 1.0], "Flash Open Strobe", 1080, 1920, 1.0);
    flashSolid.startTime = 0.0;
    var flashOpacity = flashSolid.property("Opacity");
    flashOpacity.setValueAtTime(0.00, 100);
    flashOpacity.setValueAtTime(0.08, 90);
    flashOpacity.setValueAtTime(0.22, 0);

    // 3. Viewfinder REC HUD Overlay
    var hudText = comp.layers.addText("● REC  00:00:01:14  4K RAW");
    hudText.name = "Viewfinder REC Overlay";
    var hudProp = hudText.property("Source Text");
    var hudDoc = hudProp.value;
    hudDoc.fontSize = 28;
    hudDoc.fillColor = [1.0, 0.2, 0.2];
    hudDoc.font = "Arial-BoldMT";
    hudProp.setValue(hudDoc);
    hudText.property("Position").setValue([120, 100]);

    // 4. Kinetic Poster Title Punch Layer
    var titleLayer = comp.layers.addText("BILL ACKMAN");
    titleLayer.name = "Poster Title Punch (Kinetic)";
    titleLayer.startTime = 1.2;
    titleLayer.outPoint = 4.8;
    titleLayer.motionBlur = true;

    var titleProp = titleLayer.property("Source Text");
    var titleDoc = titleProp.value;
    titleDoc.fontSize = 76;
    titleDoc.font = "Impact";
    titleDoc.fillColor = [1.0, 0.875, 0.22];
    titleDoc.strokeColor = [0.0, 0.0, 0.0];
    titleDoc.strokeWidth = 4;
    titleDoc.applyStroke = true;
    titleDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    titleProp.setValue(titleDoc);

    // Center Anchor & Keyframed Impact Scale Bounce
    titleLayer.property("Position").setValue([540.0, 820.0]);
    var scaleProp = titleLayer.property("Scale");
    scaleProp.setValueAtTime(1.20, [145, 145]);
    scaleProp.setValueAtTime(1.35, [95, 95]);
    scaleProp.setValueAtTime(1.48, [100, 100]);

    // 5. Chromatic Bloom Glow Filter
    if (true) {
        var glowEffect = titleLayer.property("Effects").addProperty("ADBE Glow2");
        glowEffect.property("Glow Based On").setValue(1); // Color Channels
        glowEffect.property("Glow Threshold").setValue(55);
        glowEffect.property("Glow Radius").setValue(38);
        glowEffect.property("Glow Intensity").setValue(1.85);
    }

    // 6. Screen Name Reveal Layer
    var subLayer = comp.layers.addText("PERSHING SQUARE CAPITAL");
    subLayer.name = "Screen Name Reveal (Credentials)";
    subLayer.startTime = 2.4;
    subLayer.outPoint = 6.2;
    var subProp = subLayer.property("Source Text");
    var subDoc = subProp.value;
    subDoc.fontSize = 32;
    subDoc.font = "Arial-BoldMT";
    subDoc.fillColor = [1.0, 1.0, 1.0];
    subDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    subProp.setValue(subDoc);
    subLayer.property("Position").setValue([540.0, 920.0]);

    // 7. Counter Rate (Metric Odometer Ticker)
    var counterLayer = comp.layers.addText("AUM: $18,000,000,000");
    counterLayer.name = "Counter Rate (Odometer)";
    counterLayer.startTime = 4.0;
    counterLayer.outPoint = 12.0;
    var counterProp = counterLayer.property("Source Text");
    var counterDoc = counterProp.value;
    counterDoc.fontSize = 42;
    counterDoc.font = "Impact";
    counterDoc.fillColor = [0.0, 1.0, 0.55];
    counterDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    counterProp.setValue(counterDoc);
    counterLayer.property("Position").setValue([540.0, 1600]);

    // Add Expression to Counter Layer for live tick animation
    counterLayer.property("Source Text").expression = 
        'var startVal = 0; var endVal = 18000000000; var tStart = 4.0; var tEnd = 7.0; ' +
        'var val = Math.round(linear(time, tStart, tEnd, startVal, endVal)); ' +
        '"AUM: $" + val.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");';

    // 8. Add Markers for 11 Ingredients Breakdown
    var markerTimes = [
        [0.0, "1. Flash Open"],
        [1.2, "2. Poster Title Punch"],
        [2.8, "3. Screen Name Reveal"],
        [4.5, "4. Difference Pull Back"],
        [6.2, "5. Face Match Cut"],
        [8.0, "6. Grid Cut List"],
        [10.1, "7. Quantity Or Quality"],
        [12.0, "8. Flip Stack"],
        [14.2, "9. Viewfinder REC"],
        [16.5, "10. Counter Rate"],
        [0.0, "11. Granular SFX Track"]
    ];

    for (var m = 0; m < markerTimes.length; m++) {
        var myMarker = new MarkerValue(markerTimes[m][1]);
        comp.markerProperty.setValueAtTime(markerTimes[m][0], myMarker);
    }

    app.endUndoGroup();
    alert("Pocket Creator Director: Style DNA Timeline Loaded!\nComp: " + compName);
})();
