/// Flutter-independent canvas geometry, bounded ink wire format and
/// immutable scene history. Based on Notes-Ecosistema whiteboard donor.
/// Does not provide widgets, stylus event routing, renderer or persistence.
library;
import 'dart:convert';

final class CanvasReferenceException implements Exception {
  const CanvasReferenceException(this.code);
  final String code;
  @override
  String toString() => 'CanvasReferenceException($code)';
}

final class CanvasVector {
  CanvasVector(this.x,this.y) {
    if (!x.isFinite || !y.isFinite) {
      throw const CanvasReferenceException('INVALID_COORDINATE');
    }
  }
  final double x,y;
}

final class CanvasCamera {
  CanvasCamera({
    required this.viewportWidth,
    required this.viewportHeight,
    this.centerX = 0,
    this.centerY = 0,
    this.zoom = 1,
  }) {
    if (!viewportWidth.isFinite || !viewportHeight.isFinite ||
        viewportWidth <= 0 || viewportHeight <= 0 ||
        !centerX.isFinite || !centerY.isFinite ||
        !zoom.isFinite || zoom < 0.1 || zoom > 8) {
      throw const CanvasReferenceException('INVALID_CAMERA');
    }
  }
  final double viewportWidth,viewportHeight,centerX,centerY,zoom;

  CanvasVector worldToScreen(CanvasVector point) =>
    CanvasVector((point.x-centerX)*zoom+viewportWidth/2,
                 (point.y-centerY)*zoom+viewportHeight/2);

  CanvasVector screenToWorld(CanvasVector point) =>
    CanvasVector((point.x-viewportWidth/2)/zoom+centerX,
                 (point.y-viewportHeight/2)/zoom+centerY);

  CanvasCamera panScreen(double dx,double dy) => CanvasCamera(
    viewportWidth:viewportWidth,viewportHeight:viewportHeight,
    centerX:centerX-dx/zoom,centerY:centerY-dy/zoom,zoom:zoom);

  /// Preserve the same logical world point under an arbitrary pinch anchor.
  CanvasCamera zoomAt(CanvasVector screenAnchor,double nextZoom) {
    final world=screenToWorld(screenAnchor);
    return CanvasCamera(viewportWidth:viewportWidth,viewportHeight:viewportHeight,
      centerX:world.x-(screenAnchor.x-viewportWidth/2)/nextZoom,
      centerY:world.y-(screenAnchor.y-viewportHeight/2)/nextZoom,
      zoom:nextZoom);
  }

  CanvasCamera resize(double width,double height) => CanvasCamera(
    viewportWidth:width,viewportHeight:height,
    centerX:centerX,centerY:centerY,zoom:zoom);
}

final class CanvasInkPoint {
  CanvasInkPoint(this.x,this.y,{this.pressure=1000}) {
    if (x.abs()>100000 || y.abs()>100000 || pressure<0 || pressure>1000) {
      throw const CanvasReferenceException('INVALID_INK_POINT');
    }
  }
  final int x,y,pressure;
}

final class CanvasInkStroke {
  CanvasInkStroke({
    required this.id,required this.color,required this.width,
    required List<CanvasInkPoint> points,this.highlighter=false,
  }): points=List.unmodifiable(points) {
    if (id.trim().isEmpty || id.length>200 || width<1 || width>100 ||
        points.isEmpty || points.length>50000) {
      throw const CanvasReferenceException('INVALID_STROKE');
    }
  }
  final String id;
  final int color,width;
  final bool highlighter;
  final List<CanvasInkPoint> points;
}

final class CanvasStickyNode {
  CanvasStickyNode({
    required this.id,required this.position,
    required this.text,this.width=260,this.height=160,this.linkedEntityId,
  }) {
    if(id.trim().isEmpty||id.length>200||text.length>50000||
       !width.isFinite||!height.isFinite||width<16||height<16||
       width>20000||height>20000) {
      throw const CanvasReferenceException('INVALID_NODE');
    }
  }
  final String id,text;
  final CanvasVector position;
  final double width,height;
  final String? linkedEntityId;

  CanvasStickyNode moved(CanvasVector position) => CanvasStickyNode(
    id:id,position:position,text:text,width:width,height:height,
    linkedEntityId:linkedEntityId);
}

final class CanvasScene {
  CanvasScene({List<CanvasInkStroke> strokes=const [],
               List<CanvasStickyNode> nodes=const []})
      : strokes=List.unmodifiable(strokes),nodes=List.unmodifiable(nodes) {
    if(strokes.length>3000 || nodes.length>1200 ||
      strokes.fold<int>(0,(sum,s)=>sum+s.points.length)>50000) {
      throw const CanvasReferenceException('SCENE_LIMIT_EXCEEDED');
    }
    final ids=<String>{};
    for(final stroke in strokes) {
      if(!ids.add(stroke.id)) throw const CanvasReferenceException('DUPLICATE_ID');
    }
    for(final node in nodes) {
      if(!ids.add(node.id)) throw const CanvasReferenceException('DUPLICATE_ID');
    }
  }
  final List<CanvasInkStroke> strokes;
  final List<CanvasStickyNode> nodes;

  CanvasScene addStroke(CanvasInkStroke stroke) =>
    CanvasScene(strokes:[...strokes,stroke],nodes:nodes);

  CanvasScene removeStroke(String id) =>
    CanvasScene(strokes:strokes.where((s)=>s.id!=id).toList(),nodes:nodes);

  CanvasScene upsertNode(CanvasStickyNode node) => CanvasScene(
    strokes:strokes,
    nodes:[...nodes.where((n)=>n.id!=node.id),node],
  );
}

final class CanvasEditHistory {
  CanvasEditHistory({required this.current,
    List<CanvasScene> past=const [],List<CanvasScene> future=const []})
      : past=List.unmodifiable(past),future=List.unmodifiable(future);
  final CanvasScene current;
  final List<CanvasScene> past,future;
  bool get canUndo=>past.isNotEmpty;
  bool get canRedo=>future.isNotEmpty;

  CanvasEditHistory apply(CanvasScene next,{int maxSteps=100}) {
    if(maxSteps<1||maxSteps>500) {
      throw const CanvasReferenceException('INVALID_HISTORY_LIMIT');
    }
    final history=[...past,current];
    return CanvasEditHistory(current:next,
      past:history.length>maxSteps
        ? history.sublist(history.length-maxSteps):history);
  }
  CanvasEditHistory undo() {
    if(!canUndo)return this;
    return CanvasEditHistory(current:past.last,
      past:past.sublist(0,past.length-1),
      future:[current,...future]);
  }
  CanvasEditHistory redo() {
    if(!canRedo)return this;
    return CanvasEditHistory(current:future.first,
      past:[...past,current],future:future.sublist(1));
  }
}

abstract final class CanvasSceneCodec {
  static const maxBytes=2*1024*1024;
  static String encode(CanvasScene scene) {
    final json=jsonEncode({
      'format':'golden-canvas','version':1,
      'strokes':[for(final s in scene.strokes) {
        'id':s.id,'color':s.color,'width':s.width,
        'highlighter':s.highlighter,
        'points':[for(final p in s.points)...[p.x,p.y,p.pressure]],
      }],
      'nodes':[for(final n in scene.nodes) {
        'id':n.id,'x':n.position.x,'y':n.position.y,
        'width':n.width,'height':n.height,
        'text':n.text,'linkedEntityId':n.linkedEntityId,
      }],
    });
    if(utf8.encode(json).length>maxBytes) {
      throw const CanvasReferenceException('SCENE_TOO_LARGE');
    }
    return json;
  }

  static CanvasScene decode(String raw) {
    if(utf8.encode(raw).length>maxBytes) {
      throw const CanvasReferenceException('SCENE_TOO_LARGE');
    }
    try {
      final root=jsonDecode(raw) as Map<String,dynamic>;
      if(root['format']!='golden-canvas'||root['version']!=1) {
        throw const CanvasReferenceException('UNSUPPORTED_SCENE_VERSION');
      }
      final strokes=<CanvasInkStroke>[];
      for(final item in (root['strokes'] as List<dynamic>)) {
        final data=item as Map<String,dynamic>;
        final coordinates=(data['points'] as List<dynamic>).cast<num>();
        if(coordinates.length%3!=0 || coordinates.isEmpty) {
          throw const CanvasReferenceException('INVALID_INK_WIRE');
        }
        final points=<CanvasInkPoint>[];
        for(var i=0;i<coordinates.length;i+=3) {
          points.add(CanvasInkPoint(
            coordinates[i].toInt(),coordinates[i+1].toInt(),
            pressure:coordinates[i+2].toInt()));
        }
        strokes.add(CanvasInkStroke(
          id:data['id'] as String,color:data['color'] as int,
          width:data['width'] as int,
          highlighter:data['highlighter']==true,points:points));
      }
      final nodes=<CanvasStickyNode>[];
      for(final item in (root['nodes'] as List<dynamic>)) {
        final data=item as Map<String,dynamic>;
        nodes.add(CanvasStickyNode(
          id:data['id'] as String,position:CanvasVector(
            (data['x'] as num).toDouble(),(data['y'] as num).toDouble()),
          text:data['text'] as String,
          width:(data['width'] as num).toDouble(),
          height:(data['height'] as num).toDouble(),
          linkedEntityId:data['linkedEntityId'] as String?,
        ));
      }
      return CanvasScene(strokes:strokes,nodes:nodes);
    } on CanvasReferenceException {
      rethrow;
    } catch (_) {
      throw const CanvasReferenceException('INVALID_SCENE_JSON');
    }
  }
}
