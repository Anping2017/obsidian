# 代码示例库-DOM操作

## 基础DOM操作示例

### 元素创建和插入
```javascript
// 1. 创建元素
function createElements() {
    // 创建基本元素
    var div = document.createElement('div');
    div.className = 'container';
    div.id = 'myDiv';
    
    // 创建文本节点
    var text = document.createTextNode('Hello World');
    div.appendChild(text);
    
    // 创建属性
    div.setAttribute('data-value', '123');
    div.setAttribute('aria-label', 'Container');
    
    return div;
}

// 2. 插入元素
function insertElements() {
    var container = document.getElementById('container');
    var newElement = document.createElement('div');
    newElement.textContent = 'New Element';
    
    // 使用appendChild
    container.appendChild(newElement);
    
    // 使用insertBefore
    var referenceElement = container.firstChild;
    var anotherElement = document.createElement('div');
    anotherElement.textContent = 'Another Element';
    container.insertBefore(anotherElement, referenceElement);
    
    // 使用insertAdjacentHTML
    container.insertAdjacentHTML('beforeend', '<div>HTML String</div>');
    
    // 使用insertAdjacentElement
    var adjacentElement = document.createElement('div');
    adjacentElement.textContent = 'Adjacent Element';
    container.insertAdjacentElement('afterbegin', adjacentElement);
}

// 3. 批量插入
function batchInsert() {
    var container = document.getElementById('container');
    var fragment = document.createDocumentFragment();
    
    // 创建多个元素
    for (var i = 0; i < 100; i++) {
        var div = document.createElement('div');
        div.textContent = 'Item ' + i;
        div.className = 'item';
        fragment.appendChild(div);
    }
    
    // 一次性插入
    container.appendChild(fragment);
}
```

### 元素选择和操作
```javascript
// 1. 元素选择
function selectElements() {
    // 基本选择器
    var elementById = document.getElementById('myId');
    var elementsByClass = document.getElementsByClassName('myClass');
    var elementsByTag = document.getElementsByTagName('div');
    
    // 现代选择器
    var element = document.querySelector('#myId');
    var elements = document.querySelectorAll('.myClass');
    
    // 复杂选择器
    var complexElements = document.querySelectorAll('div.container > .item:first-child');
    
    return {
        byId: elementById,
        byClass: elementsByClass,
        byTag: elementsByTag,
        modern: element,
        modernAll: elements,
        complex: complexElements
    };
}

// 2. 元素操作
function manipulateElements() {
    var element = document.getElementById('myElement');
    
    // 属性操作
    element.id = 'newId';
    element.className = 'new-class';
    element.title = 'New Title';
    
    // 自定义属性
    element.setAttribute('data-custom', 'custom-value');
    element.dataset.userId = '12345';
    
    // 样式操作
    element.style.color = 'red';
    element.style.backgroundColor = 'yellow';
    element.style.fontSize = '16px';
    
    // 类名操作
    element.classList.add('active');
    element.classList.remove('inactive');
    element.classList.toggle('visible');
    
    // 内容操作
    element.innerHTML = '<strong>Bold text</strong>';
    element.textContent = 'Plain text';
    
    return element;
}

// 3. 元素遍历
function traverseElements() {
    var container = document.getElementById('container');
    
    // 遍历子元素
    var children = container.children;
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        console.log('Child:', child.tagName, child.className);
    }
    
    // 遍历所有子节点
    var childNodes = container.childNodes;
    for (var i = 0; i < childNodes.length; i++) {
        var node = childNodes[i];
        if (node.nodeType === Node.ELEMENT_NODE) {
            console.log('Element node:', node.tagName);
        } else if (node.nodeType === Node.TEXT_NODE) {
            console.log('Text node:', node.textContent);
        }
    }
    
    // 使用for...of遍历
    for (var child of container.children) {
        console.log('Child element:', child.tagName);
    }
}
```

## 事件处理示例

### 基本事件处理
```javascript
// 1. 事件监听器
function addEventListeners() {
    var button = document.getElementById('myButton');
    
    // 添加事件监听器
    button.addEventListener('click', function(event) {
        console.log('Button clicked!');
        console.log('Event:', event);
    });
    
    // 添加多个监听器
    button.addEventListener('click', function(event) {
        console.log('Second click handler');
    });
    
    // 使用命名函数
    function handleClick(event) {
        console.log('Named function handler');
    }
    
    button.addEventListener('click', handleClick);
    
    // 移除事件监听器
    button.removeEventListener('click', handleClick);
}

// 2. 事件对象
function handleEventObject() {
    var element = document.getElementById('myElement');
    
    element.addEventListener('click', function(event) {
        console.log('Event properties:');
        console.log('Type:', event.type);
        console.log('Target:', event.target);
        console.log('Current target:', event.currentTarget);
        console.log('Time stamp:', event.timeStamp);
        console.log('Bubbles:', event.bubbles);
        console.log('Cancelable:', event.cancelable);
        
        // 鼠标事件属性
        if (event.type === 'click') {
            console.log('Client X:', event.clientX);
            console.log('Client Y:', event.clientY);
            console.log('Page X:', event.pageX);
            console.log('Page Y:', event.pageY);
        }
    });
}

// 3. 事件委托
function eventDelegation() {
    var container = document.getElementById('container');
    
    // 使用事件委托
    container.addEventListener('click', function(event) {
        var target = event.target;
        
        // 处理按钮点击
        if (target.matches('button')) {
            handleButtonClick(target);
        }
        
        // 处理链接点击
        if (target.matches('a')) {
            handleLinkClick(target);
        }
        
        // 处理特定类名的元素
        if (target.classList.contains('item')) {
            handleItemClick(target);
        }
    });
    
    function handleButtonClick(button) {
        console.log('Button clicked:', button.textContent);
    }
    
    function handleLinkClick(link) {
        console.log('Link clicked:', link.href);
    }
    
    function handleItemClick(item) {
        console.log('Item clicked:', item.dataset.id);
    }
}
```

### 高级事件处理
```javascript
// 1. 自定义事件
function customEvents() {
    var element = document.getElementById('myElement');
    
    // 创建自定义事件
    var customEvent = new CustomEvent('myCustomEvent', {
        detail: {
            message: 'Hello from custom event',
            timestamp: Date.now()
        },
        bubbles: true,
        cancelable: true
    });
    
    // 监听自定义事件
    element.addEventListener('myCustomEvent', function(event) {
        console.log('Custom event received:', event.detail);
    });
    
    // 触发自定义事件
    element.dispatchEvent(customEvent);
}

// 2. 事件节流和防抖
function eventThrottling() {
    var input = document.getElementById('searchInput');
    
    // 防抖函数
    function debounce(func, wait) {
        var timeout;
        return function executedFunction() {
            var context = this;
            var args = arguments;
            var later = function() {
                timeout = null;
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // 节流函数
    function throttle(func, limit) {
        var inThrottle;
        return function() {
            var args = arguments;
            var context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(function() {
                    inThrottle = false;
                }, limit);
            }
        };
    }
    
    // 使用防抖
    var debouncedSearch = debounce(function(event) {
        console.log('Searching for:', event.target.value);
    }, 300);
    
    input.addEventListener('input', debouncedSearch);
    
    // 使用节流
    var throttledScroll = throttle(function() {
        console.log('Scrolling');
    }, 100);
    
    window.addEventListener('scroll', throttledScroll);
}

// 3. AbortController
function useAbortController() {
    var element = document.getElementById('myElement');
    var controller = new AbortController();
    
    // 使用AbortController添加事件监听器
    element.addEventListener('click', function() {
        console.log('Click handled');
    }, { signal: controller.signal });
    
    element.addEventListener('mouseover', function() {
        console.log('Mouse over');
    }, { signal: controller.signal });
    
    // 取消所有监听器
    setTimeout(function() {
        controller.abort();
    }, 5000);
}
```

## 性能优化示例

### 批量操作
```javascript
// 1. DocumentFragment
function useDocumentFragment() {
    var container = document.getElementById('container');
    var fragment = document.createDocumentFragment();
    
    // 在内存中构建DOM
    for (var i = 0; i < 1000; i++) {
        var div = document.createElement('div');
        div.textContent = 'Item ' + i;
        div.className = 'item';
        fragment.appendChild(div);
    }
    
    // 一次性插入到DOM
    container.appendChild(fragment);
}

// 2. 隐藏元素操作
function hideDuringOperation() {
    var container = document.getElementById('container');
    
    // 隐藏元素
    container.style.display = 'none';
    
    // 执行大量DOM操作
    for (var i = 0; i < 1000; i++) {
        var div = document.createElement('div');
        div.textContent = 'Item ' + i;
        container.appendChild(div);
    }
    
    // 显示元素
    container.style.display = 'block';
}

// 3. CSS类批量修改
function useCSSClasses() {
    var elements = document.querySelectorAll('.item');
    
    // 定义CSS类
    var style = document.createElement('style');
    style.textContent = `
        .highlighted {
            color: red;
            background-color: yellow;
            font-size: 16px;
        }
    `;
    document.head.appendChild(style);
    
    // 批量应用类
    elements.forEach(function(element) {
        element.classList.add('highlighted');
    });
}
```

### 缓存和优化
```javascript
// 1. DOM引用缓存
function cacheDOMReferences() {
    // 缓存DOM引用
    var elements = {
        container: document.getElementById('container'),
        button: document.getElementById('button'),
        input: document.getElementById('input'),
        output: document.getElementById('output')
    };
    
    // 使用缓存的引用
    function updateContent() {
        elements.output.textContent = elements.input.value;
    }
    
    elements.button.addEventListener('click', updateContent);
    elements.input.addEventListener('input', updateContent);
    
    return elements;
}

// 2. 选择器缓存
function selectorCaching() {
    var cache = new Map();
    
    function cachedQuery(selector) {
        if (cache.has(selector)) {
            return cache.get(selector);
        }
        
        var elements = document.querySelectorAll(selector);
        cache.set(selector, elements);
        return elements;
    }
    
    // 使用缓存的选择器
    var buttons = cachedQuery('button');
    var inputs = cachedQuery('input');
    var links = cachedQuery('a');
    
    // 清理缓存
    function clearCache() {
        cache.clear();
    }
}

// 3. 避免强制同步布局
function avoidForcedLayout() {
    var elements = document.querySelectorAll('.item');
    
    // 先读取所有需要的值
    var measurements = [];
    elements.forEach(function(element) {
        measurements.push({
            element: element,
            width: element.offsetWidth
        });
    });
    
    // 再批量写入
    measurements.forEach(function(measurement) {
        measurement.element.style.width = '200px';
        measurement.element.style.height = measurement.width + 'px';
    });
}
```

## 现代API示例

### 观察者API
```javascript
// 1. IntersectionObserver
function useIntersectionObserver() {
    var elements = document.querySelectorAll('.observe-me');
    
    // 创建观察者
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                console.log('Element is visible:', entry.target);
                entry.target.classList.add('visible');
            } else {
                console.log('Element is hidden:', entry.target);
                entry.target.classList.remove('visible');
            }
        });
    });
    
    // 开始观察
    elements.forEach(function(element) {
        observer.observe(element);
    });
}

// 2. MutationObserver
function useMutationObserver() {
    var element = document.getElementById('myElement');
    
    // 创建观察者
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            console.log('Mutation type:', mutation.type);
            console.log('Target:', mutation.target);
            
            if (mutation.type === 'childList') {
                console.log('Added nodes:', mutation.addedNodes);
                console.log('Removed nodes:', mutation.removedNodes);
            }
            
            if (mutation.type === 'attributes') {
                console.log('Attribute:', mutation.attributeName);
                console.log('Old value:', mutation.oldValue);
            }
        });
    });
    
    // 开始观察
    observer.observe(element, {
        childList: true,
        attributes: true,
        attributeOldValue: true,
        subtree: true
    });
}

// 3. ResizeObserver
function useResizeObserver() {
    var elements = document.querySelectorAll('.resize-me');
    
    // 创建观察者
    var observer = new ResizeObserver(function(entries) {
        entries.forEach(function(entry) {
            var element = entry.target;
            var width = entry.contentRect.width;
            var height = entry.contentRect.height;
            
            console.log('Element resized:', {
                element: element,
                width: width,
                height: height
            });
            
            // 根据大小调整样式
            if (width < 300) {
                element.classList.add('small');
            } else {
                element.classList.remove('small');
            }
        });
    });
    
    // 开始观察
    elements.forEach(function(element) {
        observer.observe(element);
    });
}
```

### Web Animations API
```javascript
// 1. 基本动画
function basicWebAnimations() {
    var element = document.getElementById('myElement');
    
    // 创建动画
    var animation = element.animate([
        { transform: 'translateX(0px)', opacity: 1 },
        { transform: 'translateX(100px)', opacity: 0.5 },
        { transform: 'translateX(200px)', opacity: 1 }
    ], {
        duration: 1000,
        easing: 'ease-in-out',
        iterations: Infinity,
        direction: 'alternate'
    });
    
    // 控制动画
    animation.play();
    
    // 暂停动画
    setTimeout(function() {
        animation.pause();
    }, 5000);
    
    // 取消动画
    setTimeout(function() {
        animation.cancel();
    }, 10000);
}

// 2. 动画序列
function animationSequence() {
    var elements = document.querySelectorAll('.animate-me');
    
    // 创建动画序列
    var animations = [];
    
    elements.forEach(function(element, index) {
        var animation = element.animate([
            { transform: 'translateY(0px)', opacity: 0 },
            { transform: 'translateY(-20px)', opacity: 1 }
        ], {
            duration: 500,
            delay: index * 100,
            fill: 'forwards'
        });
        
        animations.push(animation);
    });
    
    // 等待所有动画完成
    Promise.all(animations.map(function(anim) {
        return anim.finished;
    })).then(function() {
        console.log('All animations completed');
    });
}
```

## 实用工具函数

### DOM工具函数
```javascript
// 1. 元素工具函数
var DOMUtils = {
    // 创建元素
    create: function(tag, attributes, content) {
        var element = document.createElement(tag);
        
        if (attributes) {
            Object.keys(attributes).forEach(function(key) {
                if (key === 'className') {
                    element.className = attributes[key];
                } else if (key === 'innerHTML') {
                    element.innerHTML = attributes[key];
                } else {
                    element.setAttribute(key, attributes[key]);
                }
            });
        }
        
        if (content) {
            element.textContent = content;
        }
        
        return element;
    },
    
    // 查找元素
    find: function(selector, context) {
        context = context || document;
        return context.querySelector(selector);
    },
    
    // 查找所有元素
    findAll: function(selector, context) {
        context = context || document;
        return context.querySelectorAll(selector);
    },
    
    // 添加类名
    addClass: function(element, className) {
        element.classList.add(className);
    },
    
    // 移除类名
    removeClass: function(element, className) {
        element.classList.remove(className);
    },
    
    // 切换类名
    toggleClass: function(element, className) {
        element.classList.toggle(className);
    },
    
    // 检查类名
    hasClass: function(element, className) {
        return element.classList.contains(className);
    },
    
    // 设置样式
    setStyle: function(element, styles) {
        Object.keys(styles).forEach(function(key) {
            element.style[key] = styles[key];
        });
    },
    
    // 获取样式
    getStyle: function(element, property) {
        return window.getComputedStyle(element)[property];
    }
};

// 2. 事件工具函数
var EventUtils = {
    // 添加事件监听器
    on: function(element, event, handler, options) {
        element.addEventListener(event, handler, options);
    },
    
    // 移除事件监听器
    off: function(element, event, handler) {
        element.removeEventListener(event, handler);
    },
    
    // 一次性事件监听器
    once: function(element, event, handler) {
        var onceHandler = function(e) {
            handler(e);
            element.removeEventListener(event, onceHandler);
        };
        element.addEventListener(event, onceHandler);
    },
    
    // 事件委托
    delegate: function(container, selector, event, handler) {
        container.addEventListener(event, function(e) {
            if (e.target.matches(selector)) {
                handler.call(e.target, e);
            }
        });
    },
    
    // 防抖
    debounce: function(func, wait) {
        var timeout;
        return function executedFunction() {
            var context = this;
            var args = arguments;
            var later = function() {
                timeout = null;
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 节流
    throttle: function(func, limit) {
        var inThrottle;
        return function() {
            var args = arguments;
            var context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(function() {
                    inThrottle = false;
                }, limit);
            }
        };
    }
};

// 3. 动画工具函数
var AnimationUtils = {
    // 淡入
    fadeIn: function(element, duration) {
        duration = duration || 300;
        element.style.opacity = '0';
        element.style.display = 'block';
        
        var start = performance.now();
        function animate(time) {
            var elapsed = time - start;
            var progress = Math.min(elapsed / duration, 1);
            element.style.opacity = progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        requestAnimationFrame(animate);
    },
    
    // 淡出
    fadeOut: function(element, duration) {
        duration = duration || 300;
        var start = performance.now();
        var startOpacity = parseFloat(element.style.opacity) || 1;
        
        function animate(time) {
            var elapsed = time - start;
            var progress = Math.min(elapsed / duration, 1);
            element.style.opacity = startOpacity * (1 - progress);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.display = 'none';
            }
        }
        requestAnimationFrame(animate);
    },
    
    // 滑动
    slideDown: function(element, duration) {
        duration = duration || 300;
        element.style.height = '0px';
        element.style.display = 'block';
        element.style.overflow = 'hidden';
        
        var targetHeight = element.scrollHeight;
        var start = performance.now();
        
        function animate(time) {
            var elapsed = time - start;
            var progress = Math.min(elapsed / duration, 1);
            element.style.height = (targetHeight * progress) + 'px';
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.height = 'auto';
                element.style.overflow = 'visible';
            }
        }
        requestAnimationFrame(animate);
    }
};
```

## 相关链接
- [[03-应用实践层/01-DOM操作/01-DOM树结构]] - DOM树基础
- [[03-应用实践层/01-DOM操作/02-元素选择与操作]] - 元素选择方法
- [[03-应用实践层/01-DOM操作/03-事件处理机制]] - 事件处理详解
- [[03-应用实践层/01-DOM操作/04-事件委托模式]] - 事件委托优化
- [[03-应用实践层/01-DOM操作/05-性能优化技巧]] - DOM性能优化
- [[03-应用实践层/01-DOM操作/06-现代DOM API]] - 现代DOM API
