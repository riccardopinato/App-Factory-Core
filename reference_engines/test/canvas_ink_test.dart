import 'package:golden_reference_engines/golden_reference_engines.dart';
import 'package:test/test.dart';

void main() {
  final origin=CanvasVector(0,0);
  test('logical origin is always at center of initial viewport',() {
    final camera=CanvasCamera(viewportWidth:400,viewportHeight:300);
    final center=camera.worldToScreen(origin);
    expect(center.x,200);expect(center.y,150);
    final roundtrip=camera.screenToWorld(center);
    expect(roundtrip.x,0);expect(roundtrip.y,0);
  });
  test('pan and anchored pinch preserve world positions at 2x zoom',() {
    final camera=CanvasCamera(viewportWidth:400,viewportHeight:300);
    final anchor=CanvasVector(280,180);
    final world=camera.screenToWorld(anchor);
    final zoomed=camera.zoomAt(anchor,2);
    expect(zoomed.screenToWorld(anchor).x,closeTo(world.x,1e-8));
    expect(zoomed.screenToWorld(anchor).y,closeTo(world.y,1e-8));
    final panned=zoomed.panScreen(100,40);
    expect(panned.centerX,closeTo(zoomed.centerX-50,1e-8));
    expect(panned.centerY,closeTo(zoomed.centerY-20,1e-8));
    expect(zoomed.resize(800,600).centerX,zoomed.centerX);
    expect(()=>camera.zoomAt(anchor,0),throwsA(isA<CanvasReferenceException>()));
  });
  CanvasInkStroke stroke(String id) => CanvasInkStroke(id:id,
    color:0xff000000,width:4,
    points:[CanvasInkPoint(1,2,pressure:500),CanvasInkPoint(-2,4,pressure:800)]);
  test('immutable scene history and ink wire roundtrip',() {
    final original=CanvasScene();
    final one=original.addStroke(stroke('ink'));
    final withNode=one.upsertNode(CanvasStickyNode(id:'sticky',
      position:CanvasVector(10,20),text:'Hello',linkedEntityId:'note-1'));
    var history=CanvasEditHistory(current:original);
    history=history.apply(one).apply(withNode);
    expect(history.undo().current.nodes,isEmpty);
    expect(history.undo().redo().current.nodes,hasLength(1));
    final restored=CanvasSceneCodec.decode(CanvasSceneCodec.encode(withNode));
    expect(restored.strokes.single.points.last.pressure,800);
    expect(restored.nodes.single.linkedEntityId,'note-1');
    expect(restored.removeStroke('ink').strokes,isEmpty);
  });
  test('limit and malformed wire fail closed',() {
    expect(()=>CanvasScene(strokes:[stroke('x'),stroke('x')]),
      throwsA(isA<CanvasReferenceException>()));
    expect(()=>CanvasSceneCodec.decode('{"format":"golden-canvas","version":99,"strokes":[],"nodes":[]}'),
      throwsA(isA<CanvasReferenceException>().having((e)=>e.code,'code',
        'UNSUPPORTED_SCENE_VERSION')));
    expect(()=>CanvasSceneCodec.decode('{"format":"golden-canvas","version":1,"strokes":[{"id":"a","color":0,"width":1,"points":[1,2]}],"nodes":[]}'),
      throwsA(isA<CanvasReferenceException>().having((e)=>e.code,'code',
        'INVALID_INK_WIRE')));
    expect(()=>CanvasSceneCodec.decode('{broken'),
      throwsA(isA<CanvasReferenceException>()));
    expect(()=>CanvasCamera(viewportWidth:300,viewportHeight:0),
      throwsA(isA<CanvasReferenceException>()));
  });
  test('bounded 20k ink points roundtrip with exact count',() {
    final points=List.generate(20000,(i)=>CanvasInkPoint(i%1000,i~/1000));
    final scene=CanvasScene(strokes:[
      CanvasInkStroke(id:'big',color:0xff123456,width:2,points:points),
    ]);
    final decoded=CanvasSceneCodec.decode(CanvasSceneCodec.encode(scene));
    expect(decoded.strokes.single.points.length,20000);
    expect(decoded.strokes.single.points.last.x,999);
  });
}
