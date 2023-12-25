from meerk40t.gui.icons import icon_meerk40t


def plugin(service, lifecycle):
    if lifecycle == "invalidate":
        return not service.has_feature("wx")
    if lifecycle == "service":
        return "provider/device/silhouette"
    if lifecycle == "added":
        # Define GUI information here.

        import wx

        def popup_info(event):
            dlg = wx.MessageDialog(
                None,
                "This is the device for Silhouette vinyl cutters!",
                "Silhouette",
                wx.OK | wx.ICON_WARNING,
            )
            dlg.ShowModal()
            dlg.Destroy()

        service.register(
            "button/control/Info",
            {
                "label": "Silhouette Vinyl Cutter",
                "icon": icon_meerk40t,
                "tip": "Provide information about the Silhouette vinyl cutter",
                "action": popup_info,
            },
        )
