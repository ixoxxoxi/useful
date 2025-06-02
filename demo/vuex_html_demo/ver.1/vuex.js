// vuex.js
class Store {
  constructor(options) {
    this._state = Vue.reactive(options.state || {});
    this._mutations = {};
    this._actions = {};
    this._getters = {};
    this._modules = new ModuleCollection(options);
    
    installModule(this, this._state, [], this._modules.root);
    
    this.getters = Vue.reactive(this._getters);
  }
  
  get state() {
    return this._state;
  }
  
  commit(type, payload) {
    const mutation = this._mutations[type];
    if (mutation) {
      mutation(payload);
    } else {
      console.error(`[vuex] unknown mutation type: ${type}`);
    }
  }
  
  dispatch(type, payload) {
    const action = this._actions[type];
    if (action) {
      return action(payload);
    } else {
      console.error(`[vuex] unknown action type: ${type}`);
      return Promise.reject(new Error(`Unknown action type: ${type}`));
    }
  }
  
  install(app) {
    app.config.globalProperties.$store = this;
  }
}

class Module {
  constructor(rawModule) {
    this._children = {};
    this._rawModule = rawModule;
    this.state = Vue.reactive(rawModule.state || {});
    this.namespaced = !!rawModule.namespaced;
  }
  
  getChild(key) {
    return this._children[key];
  }
  
  addChild(key, module) {
    this._children[key] = module;
  }
}

class ModuleCollection {
  constructor(rawRootModule) {
    this.rootModule = null;
    this.register([], rawRootModule);
  }
  
  get root() {
    return this.rootModule;
  }
  
  register(path, rawModule) {
    const newModule = new Module(rawModule);
    
    if (path.length === 0) {
      this.rootModule = newModule;
    } else {
      const parent = this.get(path.slice(0, -1));
      parent.addChild(path[path.length - 1], newModule);
    }
    
    if (rawModule.modules) {
      Object.keys(rawModule.modules).forEach(key => {
        this.register(path.concat(key), rawModule.modules[key]);
      });
    }
  }
  
  get(path) {
    return path.reduce((module, key) => {
      return module.getChild(key);
    }, this.rootModule);
  }
}

function installModule(store, rootState, path, module) {
  const namespace = getNamespace(path);
  
  if (path.length > 0) {
    const parentState = getParentState(rootState, path.slice(0, -1));
    const moduleName = path[path.length - 1];
    
    if (!parentState[moduleName]) {
      parentState[moduleName] = Vue.reactive({});
    }
    
    Object.assign(parentState[moduleName], module.state);
  }
  
  // Mutations
  if (module._rawModule.mutations) {
    Object.entries(module._rawModule.mutations).forEach(([key, mutation]) => {
      const namespacedType = namespace + key;
      store._mutations[namespacedType] = (payload) => {
        mutation(module.state, payload);
      };
    });
  }
  
  // Actions
  if (module._rawModule.actions) {
    Object.entries(module._rawModule.actions).forEach(([key, action]) => {
      const namespacedType = namespace + key;
      store._actions[namespacedType] = (payload) => {
        return action({
          state: module.state,
          rootState,
          commit: createNamespacedCommit(store, namespace),
          dispatch: createNamespacedDispatch(store, namespace),
          getters: store.getters
        }, payload);
      };
    });
  }
  
  // Getters
  if (module._rawModule.getters) {
    Object.entries(module._rawModule.getters).forEach(([key, getter]) => {
      const namespacedType = namespace + key;
      Object.defineProperty(store._getters, namespacedType, {
        get: () => getter(module.state, store.getters, rootState),
        enumerable: true
      });
    });
  }
  
  // 递归安装子模块
  Object.entries(module._children).forEach(([key, child]) => {
    installModule(store, rootState, path.concat(key), child);
  });
}

function getNamespace(path) {
  return path.length ? path.join('/') + '/' : '';
}

function getParentState(rootState, path) {
  return path.length ? path.reduce((state, key) => state[key], rootState) : rootState;
}

function createNamespacedCommit(store, namespace) {
  return (type, payload) => {
    store.commit(namespace + type, payload);
  };
}

function createNamespacedDispatch(store, namespace) {
  return (type, payload) => {
    return store.dispatch(namespace + type, payload);
  };
}

// 辅助函数
function mapState(namespace, states) {
  const result = {};
  states.forEach(key => {
    result[key] = function() {
      return namespace 
        ? this.$store.state[namespace][key]
        : this.$store.state[key];
    };
  });
  return result;
}

function mapGetters(namespace, getters) {
  const result = {};
  getters.forEach(key => {
    result[key] = function() {
      const fullKey = namespace ? `${namespace}/${key}` : key;
      return this.$store.getters[fullKey];
    };
  });
  return result;
}

function mapMutations(namespace, mutations) {
  const result = {};
  mutations.forEach(key => {
    result[key] = function(payload) {
      const fullKey = namespace ? `${namespace}/${key}` : key;
      this.$store.commit(fullKey, payload);
    };
  });
  return result;
}

function mapActions(namespace, actions) {
  const result = {};
  actions.forEach(key => {
    result[key] = function(payload) {
      const fullKey = namespace ? `${namespace}/${key}` : key;
      return this.$store.dispatch(fullKey, payload);
    };
  });
  return result;
}

// 创建 store 的函数
function createStore(options) {
  return new Store(options);
}