from pyramid.httpexceptions import HTTPForbidden

import ptah
from ptah import view, config, form
from ptah.authentication import auth_service

CONFIG_ID = 'ptah.manage:config'
MANAGE_ID = 'ptah.manage:module'
INTROSPECT_ID = 'ptah.manage:introspection'


ptah.register_settings(
    ptah.CFG_ID_MANAGE,

    form.LinesField(
        'managers',
        title = 'Managers',
        description = 'List of user logins with access rights to '\
            'ptah management ui.',
        default = ()),

    form.TextField(
        name = 'manage_url',
        title = 'Ptah manage url',
        default = '/ptah-manage'),

    form.LinesField(
        'disable_modules',
        title = 'Hide Modules in Management UI',
        description = 'List of modules names to hide in manage ui',
        default = ()),

    form.LinesField(
        'disable_models',
        title = 'Hide Models in Model Management UI',
        description = 'List of models to hide in model manage ui',
        default = ('cms-type:sqlblob',)),

    title = 'Ptah manage settings',
    )


class PtahModule(object):

    #: Module name (also is used for url generation)
    name = ''

    #: Module title
    title = ''

    def __init__(self, manager, request):
        self.__parent__ = manager
        self.request = request

    def url(self):
        """ return url to this module """
        cfg = ptah.get_settings(ptah.CFG_ID_MANAGE, self.request.registry)
        return '%s/%s'%(cfg['manage_url'], self.name)

    @property
    def __name__(self):
        return self.name

    def available(self):
        """ is module available """
        return True


def module(id):
    info = config.DirectiveInfo()

    def wrapper(cls):
        def _complete(cfg, cls, id):
            cls.name = id
            cfg.get_cfg_storage(MANAGE_ID)[id] = cls

        info.attach(
            config.Action(
                _complete, (cls, id,),
                discriminator = (MANAGE_ID, id))
            )
        return cls

    return wrapper


def intr_renderer(id):
    info = config.DirectiveInfo()

    def wrapper(cls):
        def _complete(cfg, cls, id):
            cls.name = id
            cfg.get_cfg_storage(INTROSPECT_ID)[id] = cls

        info.attach(
            config.Action(
                _complete, (cls, id,),
                discriminator = (INTROSPECT_ID, id))
            )
        return cls

    return wrapper


def PtahAccessManager(id):
    """ default access manager """
    cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)

    managers = cfg['managers']
    if '*' in managers:
        return True

    principal = ptah.resolve(id)

    if principal is not None and principal.login in managers:
        return True

    return False


def check_access(userid):
    cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)
    return cfg.get('access_manager', PtahAccessManager)(userid)


def set_access_manager(func):
    cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)
    cfg['access_manager'] = func


class PtahManageRoute(object):
    """ ptah management route """

    __name__ = 'ptah-manage'
    __parent__ = None

    def __init__(self, request):
        self.request = request

        userid = auth_service.get_userid()
        if not check_access(userid):
            raise HTTPForbidden()

        self.userid = userid
        self.cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)
        self.manage_url = self.cfg['manage_url']

        auth_service.set_effective_userid(ptah.SUPERUSER_URI)

    def __getitem__(self, key):
        if key not in self.cfg['disable_modules']:
            mod = config.get_cfg_storage(MANAGE_ID).get(key)

            if mod is not None:
                return mod(self, self.request)

        raise KeyError(key)


view.snippettype('ptah-module-actions', PtahModule)

view.register_snippet(
    'ptah-module-actions', PtahModule,
    template = view.template('ptah.manage:templates/moduleactions.pt'))

view.register_layout(
    '', PtahManageRoute, parent='ptah-manage',
    template=view.template("ptah.manage:templates/ptah-layout.pt"))

view.register_layout(
    'ptah-page', PtahManageRoute, parent='ptah-manage',
    template=view.template("ptah.manage:templates/ptah-layout.pt"))


class LayoutManage(view.Layout):
    view.layout('ptah-manage', PtahManageRoute,
                template=view.template("ptah.manage:templates/ptah-manage.pt"))

    def update(self):
        self.cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)
        self.manage_url = self.cfg['manage_url']
        self.user = ptah.resolve(self.context.userid)

        mod = self.request.context
        while not isinstance(mod, PtahModule):
            mod = getattr(mod, '__parent__', None)
            if mod is None: # pragma: no cover
                break

        self.module = mod


class ManageView(view.View):
    """List ptah modules"""
    view.pview(
        context = PtahManageRoute,
        template = view.template('ptah.manage:templates/manage.pt'))

    __intr_path__ = '/ptah-manage/'

    rst_to_html = staticmethod(ptah.rst_to_html)

    def update(self):
        context = self.context
        request = self.request
        self.cfg = ptah.get_settings(ptah.CFG_ID_MANAGE)

        mods = []
        for name, mod in config.get_cfg_storage(MANAGE_ID).items():
            if name in self.cfg['disable_modules']:
                continue
            mod = mod(context, request)
            if not mod.available():
                continue
            mods.append((mod.title, mod))

        self.modules = [mod for _t, mod in sorted(mods)]
