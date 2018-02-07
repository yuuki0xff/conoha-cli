conoha-cli
==========
**conoha-cli** は `ConoHa <https://www.conoha.jp/>`_ API のコマンドラインインターフェースとPython3用ライブラリです。

インストール
============
`conoha-cli` はこのコマンドを実行するとインストールでいます::

    $ pip3 install conoha-cli

次に、`~/.config/conoha/config` へこのようなファイルを作成してください。
user, passwd, tenantは、`Conohaコントロールパネルから作成したAPIユーザ <https://www.conoha.jp/guide/g-46.html>`_ の値を入力してください。::

    [api]
    user = xxxxx
    passwd = xxxxx
    tenant = xxxxx

使い方
======
VPSの一覧を確認する::

    $ conoha-cli compute list-vms

マシンリーダブルな形式でも出力できます::

    $ conoha-cli --format plain --header no compute list-vms

VPSを起動・終了・削除する::

    $ conoha-cli compute start-vm $VM_NAME
    $ conoha-cli compute stop-vm  $VM_NAME
    $ conoha-cli compute delete-vm $VM_NAME

ライセンス
==========
MIT
