---
title: Three三维世界初体验
date: 2019-01-03 15:26:03
tags: 
- 前端
- Three.js
- WebGL
categories: 前端
---
教程：
[WebGL中文网教程](http://www.hewebgl.com/article/articledir/1)
[three文档](https://threejs.org/docs/index.html#manual/en/introduction/Creating-a-scene)
[碰撞检测](https://blog.csdn.net/linolzhang/article/details/67119049)
原理：
以物体的中心为起点，向各个顶点（vertices）发出射线，如果射线与其它的物体相交，则检查最近的一个交点与射线起点间的距离，如果这个距离比射线起点至物体顶点间的距离要小，则说明发生了碰撞。但是，当物体的中心在另一个物体内部时，是不能够检测到碰撞的。而且当两个物体能够互相穿过，且有较大部分重合时，检测效果也不理想。 

![代码示例](https://upload-images.jianshu.io/upload_images/14827444-3b266c643b2f3f13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![碰撞实例](https://upload-images.jianshu.io/upload_images/14827444-99942b6d2eb3e777.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
    // 初始化Three
    var renderer;
    function initThree() {
        renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);

        width = document.getElementById('canvas-frame').clientWidth;
        height = document.getElementById('canvas-frame').clientHeight;
        renderer = new THREE.WebGLRenderer({
            antialias : true
        });
        renderer.setSize(width, height);
        document.getElementById('canvas-frame').appendChild(renderer.domElement);
        renderer.setClearColor(0xffffff, 1.0);
    }

    // 初始化Camera
    var camera;
    function initCamera() {
        // 设置透视相机
        camera = new THREE.PerspectiveCamera(45, width / height, 1, 10000);
        // 设置相机位置
        camera.position.x = 200;
        camera.position.y = 500;
        camera.position.z = 800;
        // 设置相机哪里为上
        // camera.up.x = 0;
        // camera.up.y = 0;
        // camera.up.z = 1;
        // 设置相机看向哪
        camera.lookAt(new THREE.Vector3(0, 0, 0));
    }

    // 初始化场景
    var scene;
    function initScene() {
        scene = new THREE.Scene();
    }

    // 初始化灯光
    var light;
    function initLight() {
        light = new THREE.DirectionalLight(0xFF0000,1);
        light.position.set(100,100,1);
        scene.add(light);
    }

    // 初始化里面的元素
    var cube;
    var mesh;
    function initObject() {
        for(var k =0;k<2;k++){
            // 一个几何体
            var geometry = new THREE.BoxGeometry( 100,100,100);
            // 不同面设置不同颜色
            for ( var i = 0; i < geometry.faces.length; i += 2 ) {

                var hex = Math.random() * 0xffffff;
                geometry.faces[ i ].color.setHex( hex );
                geometry.faces[ i + 1 ].color.setHex( hex );

            }
            // 设置纹理
            // var material = new THREE.MeshBasicMaterial( { vertexColors: THREE.FaceColors} );
            var material = new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } )
            // 把几何体跟纹理混合起来
            mesh = new THREE.Mesh( geometry,material);
            // 元素的位置
            mesh.position.set(0,k*50,k * 400);
            // 把元素加到场景里
            scene.add(mesh);
        }
    }

    // 渲染
    var stats;
    function render()
    {
        // renderer.clear();
        // mesh.position.x =mesh.position.x +1;
        renderer.render(scene, camera);
        requestAnimationFrame(render);
        stats.update();
        // TWEEN.update();
    }

    // 性能检测
    function initStats(){
        stats = new Stats();
        stats.setMode(1); // 0: fps, 1: ms
    // 将stats的界面对应左上角
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.left = '0px';
        stats.domElement.style.top = '0px';
        document.body.appendChild( stats.domElement );
        setInterval( function () {
            stats.begin();
            // 你的每一帧的代码
            stats.end();
        }, 1000 / 60 );
    }

    // 初始化网格
    function initGrid(){
        // 网格的边长是1000，每个小网格的边长是50
        var helper = new THREE.GridHelper( 1000, 50,0x0000ff, 0x808080 );
        var helper2 = new THREE.GridHelper( 1000, 50,0x0000ff, 0x808080 );
        helper2.rotation.x = Math.PI/2;
        scene.add( helper );
        scene.add(helper2);
    }

    // 初始化事件
    var INTERSECTED;
    function initEvent(){
        var objects=[];
        var raycaster = new THREE.Raycaster();
        var mouse = new THREE.Vector2();
        //监听全局点击事件,通过ray检测选中哪一个object
        document.addEventListener("mousedown", (event) => {
            console.log('mousedown');
            event.preventDefault();
            mouse.x = (event.clientX / this.renderer.domElement.clientWidth) * 2 - 1;
            mouse.y = - (event.clientY / this.renderer.domElement.clientHeight) * 2 + 1;

            raycaster.setFromCamera(mouse, this.camera);
            this.scene.children.forEach(child => {
                if (child instanceof THREE.Mesh) {//根据需求判断哪些加入objects,也可以在生成object的时候push进objects
                    objects.push(child)
                }
            })
            var intersects = raycaster.intersectObjects(objects);


            if (intersects.length > 0) {
                if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );

                INTERSECTED = intersects[ 0 ].object;
                INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
                INTERSECTED.material.emissive.setHex( 0x0000ff );
            }
            else {
                if ( INTERSECTED ) {
                    INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
                    // 碰撞检测
                    var originPoint = INTERSECTED.position.clone();
                    var crash = false;
                    for (var vertexIndex = 0; vertexIndex < INTERSECTED.geometry.vertices.length; vertexIndex++) {
                        // 顶点原始坐标
                        var localVertex = INTERSECTED.geometry.vertices[vertexIndex].clone();
                        // 顶点经过变换后的坐标
                        var globalVertex = localVertex.applyMatrix4(INTERSECTED.matrix);
                        // 获得由中心指向顶点的向量
                        var directionVector = globalVertex.sub(INTERSECTED.position);

                        // 将方向向量初始化
                        var ray = new THREE.Raycaster(originPoint, directionVector.clone().normalize());
                        // 检测射线与多个物体的相交情况

                        var collisionResults = ray.intersectObjects(objects);
                        // 如果返回结果不为空，且交点与射线起点的距离小于物体中心至顶点的距离，则发生了碰撞
                        if (collisionResults.length > 0 && collisionResults[0].distance < directionVector.length()) {
                            crash = true;

                        }
                    }
                    if(crash){
                        alert('crash');
                        INTERSECTED.position.set(0,0,400);
                    }
                }
                INTERSECTED = null;

            }
        }, false);

        document.addEventListener("mousemove",(event) => {
            event.preventDefault();
            if(INTERSECTED){
                
                var mouse = new THREE.Vector2();
                console.log(( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );
                mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );

                raycaster.setFromCamera( mouse, camera );
                var objects = [];
                scene.children.forEach(child => {
                    if (child instanceof THREE.GridHelper) {
                        objects.push(child)
                    }
                });

                var intersects = raycaster.intersectObjects( objects );

                if (intersects.length > 0) {
                    var selected = intersects[ 0 ];
                    // console.log(selected.point.x,selected.point.y,selected.point.z);
                    INTERSECTED.position.copy(selected.point);
                    INTERSECTED.position.divideScalar( 50 ).floor().multiplyScalar( 50 ).addScalar( 25 );
                }
            }
        },false);
    }

    // 动画组件
    function initTween(){
        new TWEEN.Tween( mesh.position)
            .to( { x: -400,z:100,y:100 }, 3000 ).repeat( Infinity ).start();
    }


    function threeStart() {
        initThree();
        initCamera();
        initScene();
        initLight();
        initObject();
        initGrid();
        initStats();
        initEvent();
        // initTween();
        render();
    }

    threeStart();


```

拖拽优化：
使用three-drag-controller,替代mousemove时间监听
```
    import DragControls from 'three-dragcontrols';
    import OrbitControls from 'three-orbitcontrols';
    ......
    function initDragControls() {
        // 初始化拖拽控件
        var dragControls = new DragControls(meshList, camera, renderer.domElement);
        var controls = new OrbitControls(camera, renderer.domElement);
        
        // 鼠标略过事件
        dragControls.addEventListener('hoveron', function (event) {
           
        });
        // 开始拖拽
        dragControls.addEventListener('dragstart', function (event) {
            controls.enabled = false;
        });
        // 拖拽结束
        dragControls.addEventListener('dragend', function (event) {
            controls.enabled = true;
            // crashCheck();
        });
    }

```
加入webpack管理，
优化后完整代码：
![3d](https://upload-images.jianshu.io/upload_images/14827444-f9f57f4633d3828f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
    var THREE = require('three');
    import DragControls from 'three-dragcontrols';
    import OrbitControls from 'three-orbitcontrols';
    import TransformControls from 'threejs-transformcontrols';

    // 初始化Three
    var renderer;
    var width,height;
    function initThree() {
        renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);

        width = document.getElementById('canvas-frame').clientWidth;
        height = document.getElementById('canvas-frame').clientHeight;
        renderer = new THREE.WebGLRenderer({
            antialias : true
        });
        renderer.setSize(width, height);
        document.getElementById('canvas-frame').appendChild(renderer.domElement);
        renderer.setClearColor(0xffffff, 1.0);
    }

    // 初始化Camera
    var camera;
    function initCamera() {
        // 设置透视相机
        camera = new THREE.PerspectiveCamera(45, width / height, 1, 10000);
        // 设置相机位置
        camera.position.x = 800;
        camera.position.y = 0;
        camera.position.z = 1000;
        // 设置相机哪里为上
        // camera.up.x = 0;
        // camera.up.y = 0;
        // camera.up.z = 1;
        // 设置相机看向哪
        camera.lookAt(new THREE.Vector3(0, 0, 0));
    }

    // 初始化场景
    var scene;
    function initScene() {
        scene = new THREE.Scene();
    }

    // 初始化灯光
    var light;
    function initLight() {
        light = new THREE.DirectionalLight(0xFF0000,1);
        light.position.set(100,100,1);
        scene.add(light);
    }

    // 初始化里面的元素
    var cube;
    var bus;
    var meshList = [];
    function initObject() {
        for(var k =0;k<2;k++){
            // 一个几何体
            var geometry = new THREE.BoxGeometry( 100,50,150);
            // 不同面设置不同颜色
            for ( var i = 0; i < geometry.faces.length; i += 2 ) {

                var hex = Math.random() * 0xffffff;
                geometry.faces[ i ].color.setHex( hex );
                geometry.faces[ i + 1 ].color.setHex( hex );

            }
            // 设置纹理
            // var material = new THREE.MeshBasicMaterial( { vertexColors: THREE.FaceColors} );
            var material = new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff } )
            // 把几何体跟纹理混合起来
            var mesh = new THREE.Mesh( geometry,material);
            meshList.push(mesh);
            // 元素的位置
            mesh.position.set(0,k*50,k * 400);
            // 把元素加到场景里
            scene.add(mesh);
        }
        var busGeometry = new THREE.BoxGeometry( 500,500,500);
        var butMaterial = new THREE.MeshLambertMaterial( { color: Math.random() * 0xffffff, transparent: true, opacity: 0.5} );
        bus = new THREE.Mesh(busGeometry,butMaterial);
        bus.position.set(0,0,0);
        scene.add(bus);
        var edges = new THREE.EdgesHelper( bus, 0x1535f7 );//设置边框，可以旋转
        scene.add( edges );
    }

    // 渲染
    var stats;
    function render()
    {
        // renderer.clear();
        // mesh.position.x =mesh.position.x +1;
        renderer.render(scene, camera);
        requestAnimationFrame(render);
        // stats.update();
        // TWEEN.update();
    }

    // 性能检测
    function initStats(){
        stats = new Stats();
        stats.setMode(1); // 0: fps, 1: ms
    // 将stats的界面对应左上角
        stats.domElement.style.position = 'absolute';
        stats.domElement.style.left = '0px';
        stats.domElement.style.top = '0px';
        document.body.appendChild( stats.domElement );
        setInterval( function () {
            stats.begin();
            // 你的每一帧的代码
            stats.end();
        }, 1000 / 60 );
    }

    // 初始化网格
    function initGrid(){
        // 网格的边长是1000，每个小网格的边长是50

        var helper = new THREE.GridHelper( 1000, 50,0x0000ff, 0x808080 );
        var helper2 = new THREE.GridHelper( 1000, 50,0x0000ff, 0x808080 );
        helper2.rotation.x = Math.PI/2;
        scene.add( helper );
        // scene.add(helper2);
    }

    // 初始化事件
    var INTERSECTED;
    function initEvent(){
        var objects= meshList;
        var raycaster = new THREE.Raycaster();
        var mouse = new THREE.Vector2();
        //监听全局点击事件,通过ray检测选中哪一个object
        // document.addEventListener("mousedown", (event) => {
        //     console.log('mousedown');
        //     event.preventDefault();
        //     mouse.x = (event.clientX / this.renderer.domElement.clientWidth) * 2 - 1;
        //     mouse.y = - (event.clientY / this.renderer.domElement.clientHeight) * 2 + 1;
        //
        //     raycaster.setFromCamera(mouse, this.camera);
        //     // this.scene.children.forEach(child => {
        //     //     if (child instanceof THREE.Mesh) {//根据需求判断哪些加入objects,也可以在生成object的时候push进objects
        //     //         objects.push(child)
        //     //     }
        //     // })
        //     var intersects = raycaster.intersectObjects(objects);
        //
        //
        //     if (intersects.length > 0) {
        //         if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
        //
        //         INTERSECTED = intersects[ 0 ].object;
        //         INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
        //         INTERSECTED.material.emissive.setHex( 0x0000ff );
        //     }
        //     else {
        //         if ( INTERSECTED ) {
        //             INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
        //             // 碰撞检测
        //             if(crashCheck(objects)){
        //                 alert('crash');
        //                 INTERSECTED.position.set(0,0,400);
        //             }
        //         }
        //         INTERSECTED = null;
        //
        //     }
        // }, false);

        // document.addEventListener("mousemove",(event) => {
        //     event.preventDefault();
        //     if(INTERSECTED){
        //
        //         var mouse = new THREE.Vector2();
        //         mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 );
        //         // console.log(mouse.x,mouse.y);
        //         var vector = new THREE.Vector3( mouse.x, mouse.y, 0.5 ).unproject( camera );
        //         var raycaster = new THREE.Raycaster(camera.position, vector.sub( camera.position ).normalize());
        //         var objects = [bus];
        //         // scene.children.forEach(child => {
        //         //     if (child instanceof THREE.GridHelper) {
        //         //         objects.push(child)
        //         //     }
        //         // });
        //
        //         var intersects = raycaster.intersectObjects( objects );
        //
        //
        //         if (intersects.length > 0) {
        //             var selected = intersects[ 0 ];
        //             console.log(selected.point.x,selected.point.y,selected.point.z,INTERSECTED.position.z);
        //             INTERSECTED.position.set(selected.point.x,selected.point.y,INTERSECTED.position.z);
        //             INTERSECTED.position.divideScalar( 50 ).floor().multiplyScalar( 50 ).addScalar( 25 );
        //
        //         }
        //     }
        // },false);

        var an = 1;
        document.getElementById('J_left').addEventListener('click',function(e){
            e.preventDefault();
            e.stopPropagation();
            var radius = 1000;
            an = an + 1;
            // console.log(an);
            camera.position.z = radius * Math.cos( (Math.PI / 180 ) * (an) );
            camera.position.x = radius * Math.sin( (Math.PI / 180 ) * (an) );
            camera.lookAt(new THREE.Vector3(0, 0, 0));
            // console.log('left,x='+camera.position.x+',z='+camera.position.z);
        });
        document.getElementById('J_right').addEventListener('click',function(e){
            e.preventDefault();
            e.stopPropagation();
            var radius = 1000;
            an = an - 1;
            // console.log(an);
            camera.position.z = radius * Math.cos( (Math.PI / 180 ) * (an) );
            camera.position.x = radius * Math.sin( (Math.PI / 180 ) * (an) );
            camera.lookAt(new THREE.Vector3(0, 0, 0));
            // console.log('left,x='+camera.position.x+',z='+camera.position.z);
        });
    }

    function crashCheck(objects){
        if(INTERSECTED){
            var originPoint = INTERSECTED.position.clone();
            var crash = false;
            for (var vertexIndex = 0; vertexIndex < INTERSECTED.geometry.vertices.length; vertexIndex++) {
                // 顶点原始坐标
                var localVertex = INTERSECTED.geometry.vertices[vertexIndex].clone();
                // 顶点经过变换后的坐标
                var globalVertex = localVertex.applyMatrix4(INTERSECTED.matrix);
                // 获得由中心指向顶点的向量
                var directionVector = globalVertex.sub(INTERSECTED.position);

                // 将方向向量初始化
                var ray = new THREE.Raycaster(originPoint, directionVector.clone().normalize());
                // 检测射线与多个物体的相交情况

                var collisionResults = ray.intersectObjects(objects);
                // 如果返回结果不为空，且交点与射线起点的距离小于物体中心至顶点的距离，则发生了碰撞
                if (collisionResults.length > 0 && collisionResults[0].distance < directionVector.length()) {
                    crash = true;
                }
            }
            if(crash){
                return true;
            }
        }
        return false;
    }

    // 动画组建
    function initTween(){
        new TWEEN.Tween( mesh.position)
            .to( { x: -400,z:100,y:100 }, 3000 ).repeat( Infinity ).start();
    }

    function initDragControls() {
        // 添加平移控件
        // var transformControls = new TransformControls(camera, renderer.domElement);
        // scene.add(transformControls);

        // 初始化拖拽控件
        var dragControls = new DragControls(meshList, camera, renderer.domElement);
        var controls = new OrbitControls(camera, renderer.domElement);
        
        // 鼠标略过事件
        dragControls.addEventListener('hoveron', function (event) {
            // 让变换控件对象和选中的对象绑定
            // transformControls.attach(event.object);
        });
        // 开始拖拽
        dragControls.addEventListener('dragstart', function (event) {
            controls.enabled = false;
        });
        // 拖拽结束
        dragControls.addEventListener('dragend', function (event) {
            controls.enabled = true;
            crashCheck();
        });
    }


    function threeStart() {
        initThree();
        initCamera();
        initScene();
        initLight();
        initObject();
        initGrid();
        initDragControls();
        // initStats();
        initEvent();
        // initTween();
        render();
    }

    threeStart();

```