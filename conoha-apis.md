# ConoHa APIのサポート状況

最終アップデート: 2018-02-07  
ConoHa APIのより詳しい情報は[公式ドキュメント](https://www.conoha.jp/docs/)から参照できます

サポート状況
------------
| API                      | 数         |
| ------------------------ | ---------- |
| all APIs                 | 238        |
| fully supported APIs     | 48 (20%)   |
| partially supported APIs | 2 (1%)     |
| not supported APIs       | 188 (79%)  |

Identity Service
----------------
| Support Status | Class or Method | HTTP Method | URI          | Description            |
| -------------- | --------------- | ----------- | ------------ | ---------------------- |
| not            |                 | GET         | /            | バージョン情報取得     |
| not            |                 | GET         | /v2.0        | バージョン情報詳細取得 |
| fully          | api.Token       | POST        | /v2.0/tokens | トークン発行           |

Account(Billing) Service
------------------------
| Support Status | Class or Method | HTTP Method | URI                                                 | Description                                 |
| -------------- | --------------- | ----------- | --------------------------------------------------- | ------------------------------------------- |
| not            |                 | GET         | /                                                   | バージョン情報取得                          |
| not            |                 | GET         | /v1                                                 | バージョン情報詳細取得                      |
| not            |                 | GET         | /v1/{tenant\_id}/order-items                        | アイテム一覧取得                            |
| not            |                 | GET         | /v1/{tenant\_id}/order-items/{item\_id}             | アイテム詳細取得(uu\_id 指定)               |
| not            |                 | GET         | /v1/{tenant\_id}/product-items                      | 申し込み可能商品一覧取得                    |
| not            |                 | GET         | /v1/{tenant\_id}/payment-history                    | 入金履歴取得                                |
| not            |                 | GET         | /v1/{tenant\_id}/payment-summary                    | 入金サマリー取得                            |
| not            |                 | GET         | /v1/{tenant\_id}/billing-invoices                   | 請求データ一覧取得                          |
| not            |                 | GET         | /v1/{tenant\_id}/billing-invoices/{invoice\_id}     | 請求データ明細取得(invoice\_id 指定)        |
| not            |                 | GET         | /v1/{tenant\_id}/notifications                      | 告知一覧取得                                |
| not            |                 | GET         | /v1/{tenant\_id}/notifications/{notification\_code} | 告知詳細取得(notification\_code 指定)       |
| not            |                 | PUT         | /v1/{tenant\_id}/notifications/{notification\_code} | 告知既読・未読変更                          |
| not            |                 | GET         | /v1/{tenant\_id}/object-storage/rrd/request         | Object Storage 利用状況グラフ(リクエスト数) |
| not            |                 | GET         | /v1/{tenant\_id}/object-storage/rrd/size            | Object Storage 利用状況グラフ(使用容量数)   |

Compute Service
---------------
| Support Status | Class or Method                 | HTTP Method | URI                                                                           | Description                                          |
| -------------- | ------------------------------- | ----------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| not            |                                 | GET         | /                                                                             | バージョン情報取得                                   |
| not            |                                 | GET         | /v2                                                                           | バージョン情報詳細取得                               |
| fully          | compute.VMPlanList              | GET         | /v2/{tenant\_id}/flavors                                                      | VMプラン一覧取得                                     |
| fully          | compute.VMPlanList              | GET         | /v2/{tenant\_id}/flavors/detail                                               | VMプラン詳細取得                                     |
| fully          | compute.VMPlan                  | GET         | /v2/{tenant\_id}/flavors/{flavor\_id}                                         | VMプラン詳細取得(アイテム指定)                       |
| fully          | compute.VMList                  | GET         | /v2/{tenant\_id}/servers                                                      | VM一覧取得                                           |
| fully          | compute.VMList                  | GET         | /v2/{tenant\_id}/servers/detail                                               | VM詳細取得                                           |
| fully          | compute.VM                      | GET         | /v2/{tenant\_id}/servers/{server\_id}                                         | VM詳細取得（アイテム指定)                            |
| fully          | compute.VMList.add              | POST        | /v2/{tenant\_id}/servers                                                      | VM追加                                               |
| fully          | compute.VMList.delete           | DELETE      | /v2/{tenant\_id}/servers/{server\_id}                                         | VM削除                                               |
| fully          | compute.VMList.start            | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VM起動                                               |
| fully          | compute.VMList.restart          | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VM再起動                                             |
| fully          | compute.VMList.stop(force=True) | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VM強制停止                                           |
| fully          | compute.VMList.stop()           | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VM通常停止                                           |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | OS再インストール                                     |
| fully          | compute.VMList.resize           | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VMリサイズ                                           |
| fully          | compute.VMList.resize           | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VMリサイズ（confirm）                                |
| fully          | compute.VMList.resize           | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VMリサイズ（revert）                                 |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | VNCコンソール                                        |
| fully          | compute.VM.createImage          | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ローカルディスクのイメージ保存                       |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ストレージコントローラー変更                         |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ネットワークアダプタ変更                             |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ビデオデバイスの変更                                 |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | コンソールのキーマップ変更                           |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | WEBシリアルコンソール(novaconsole)API                |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | WEBシリアルコンソール(httpconsole)API                |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ISOイメージの挿入                                    |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/action                                  | ISOイメージの排出                                    |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/os-security-groups                      | セキュリティグループのサーバへの割り当て状態表示     |
| fully          | compute.KeyList                 | GET         | /v2/{tenant\_id}/os-keypairs                                                  | キーペア一覧取得                                     |
| fully          | compute.Key                     | GET         | /v2/{tenant\_id}/os-keypairs/{keypair\_name}                                  | キーペア詳細取得(アイテム指定)                       |
| fully          | compute.KeyList.add             | POST        | /v2/{tenant\_id}/os-keypairs                                                  | キーペア追加                                         |
| fully          | compute.KeyList.delete          | DELETE      | /v2/{tenant\_id}/os-keypairs/{keypair\_name}                                  | キーペア削除                                         |
| fully          | compute.VMImageList             | GET         | /v2/{tenant\_id}/images                                                       | イメージ一覧取得                                     |
| fully          | compute.VMImageList             | GET         | /v2/{tenant\_id}/images/detail                                                | イメージ詳細取得                                     |
| fully          | compute.VMImageList             | GET         | /v2/{tenant\_id}/images/{image\_id}                                           | イメージ詳細取得(アイテム指定)                       |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/os-volume\_attachments                  | アタッチ済みボリューム一覧                           |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/os-volume\_attachments/{attachment\_id} | アタッチ済みボリューム取得（アイテム指定)            |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/os-volume\_attachments                  | ボリュームアタッチ                                   |
| not            |                                 | DELETE      | /v2/{tenant\_id}/servers/{server\_id}/os-volume\_attachments/{attachment\_id} | ボリュームデタッチ                                   |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/os-interface                            | アタッチ済みポート一覧取得                           |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/os-interface                            | アタッチ済みポート取得（アイテム指定)                |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/os-interface                            | ポートアタッチ(VMに追加IPv4アドレスを割り当て)       |
| not            |                                 | DELETE      | /v2/{tenant\_id}/servers/{server\_id}/os-interface/{attachment\_id}           | ポートデタッチ(VMに割り当てた追加IPv4アドレスを削除) |
| not            |                                 | POST        | /v2/{tenant\_id}/servers/{server\_id}/metadata                                | VMのmetadataの更新（ネームタグの変更）               |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/metadata                                | VMのmetadataの取得                                   |
| partially      | compute.VM.addressList          | GET         | /v2/{tenant\_id}/servers/{server\_id}/ips                                     | VMに紐づくアドレス一覧                               |
| partially      | compute.VM.addressList          | GET         | /v2/{tenant\_id}/servers/{server\_id}/ips/{network\_label}                    | VMに紐づくアドレス一覧(ネットワーク指定)             |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/rrd/cpu                                 | VPS利用状況グラフ（CPU使用時間）                     |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/rrd/interface                           | VPS利用状況グラフ（インターフェイストラフィック）    |
| not            |                                 | GET         | /v2/{tenant\_id}/servers/{server\_id}/rrd/disk                                | VPS利用状況グラフ（ディスクIO）                      |
| not            |                                 | GET         | /v2/{tenant\_id}/backup                                                       | バックアップ一覧取得                                 |
| not            |                                 | GET         | /v2/{tenant\_id}/backup/{backup\_id}                                          | バックアップ一覧取得(backup id 指定)                 |
| not            |                                 | POST        | /v2/{tenant\_id}/backup                                                       | バックアップの申し込み                               |
| not            |                                 | DELETE      | /v2/{tenant\_id}/backup/{backup\_id}                                          | バックアップの解約                                   |
| not            |                                 | POST        | /v2/{tenant\_id}/backup/{backup\_id}/action                                   | ブートディスクバックアップのリストア                 |
| not            |                                 | POST        | /v2/{tenant\_id}/backup/{backup\_id}/action                                   | ブート・追加ディスクバックアップのイメージ保存       |
| fully          | compute.VMImageList             | GET         | /v2/{tenant\_id}/iso-images                                                   | ISOイメージの一覧                                    |
| not            |                                 | POST        | /v2/{tenant\_id}/iso-images                                                   | ISOイメージダウンロード                              |

Block Storage Service
---------------------
| Support Status | Class or Method                 | HTTP Method | URI                                          | Description                            |
| -------------- | ------------------------------- | ----------- | -------------------------------------------- | -------------------------------------- |
| not            |                                 | GET         | /                                            | バージョン情報取得                     |
| not            |                                 | GET         | /v2                                          | バージョン情報詳細取得                 |
| fully          | compute.block.BlockTypeList     | GET         | /v2/{tenant\_id}/types                       | ボリュームタイプ一覧取得               |
| fully          | compute.block.BlockType         | GET         | /v2/{tenant\_id}/types/{volume\_type\_id}    | ボリュームタイプ取得（アイテム指定)    |
| fully          | compute.block.VolumeList        | GET         | /v2/{tenant\_id}/volumes                     | ボリューム一覧取得                     |
| fully          | compute.block.VolumeList        | GET         | /v2/{tenant\_id}/volumes/detail              | ボリューム詳細取得                     |
| fully          | compute.block.Volume            | GET         | /v2/{tenant\_id}/volumes/{volume\_id}        | ボリューム詳細取得（アイテム指定)      |
| fully          | compute.block.VolumeList.add    | POST        | /v2/{tenant\_id}/volumes                     | ボリューム作成                         |
| fully          | compute.block.VolumeList.add    | POST        | /v2/{tenant\_id}/volumes                     | ボリューム作成（ソースボリューム指定） |
| fully          | compute.block.VolumeList.delete | DELETE      | /v2/{tenant\_id}/volumes/{volume\_id}        | ボリューム削除                         |
| fully          | compute.block.Volume.save       | POST        | /v2/{tenant\_id}/volumes/{volume\_id}/action | ブロックディスクのイメージ保存         |

Image Service
-------------
| Support Status | Class or Method           | HTTP Method | URI                            | Description                                |
| -------------- | ------------------------- | ----------- | ------------------------------ | ------------------------------------------ |
|                |                           | GET         | /                              | バージョン情報取得                         |
| fully          | image.ImageList           | GET         | /v2/images                     | イメージ一覧取得(glance)                   |
| fully          | image.Image               | GET         | /v2/images/{image\_id}         | イメージ詳細取得(アイテム指定)(glance)     |
| fully          | image.Image               | GET         | /v2/schemas/images             | イメージコンテナのスキーマ情報取得         |
| fully          | image.Image               | GET         | /v2/schemas/image              | イメージのスキーマ情報取得                 |
| not            |                           | GET         | /v2/schemas/members            | イメージメンバーコンテナのスキーマ情報取得 |
| not            |                           | GET         | /v2/schemas/member             | イメージメンバーのスキーマ情報取得         |
| not            |                           | GET         | /v2/images/{image\_id}/members | イメージメンバー一覧取得                   |
| fully          | image.ImageList.delete    | DELETE      | /v2/images/{image\_id}         | イメージ削除                               |
| fully          | image.Quota.set           | PUT         | /v2/quota                      | イメージ保存容量制限                       |
| fully          | image.Quota.{region,size} | GET         | /v2/quota                      | イメージ保存容量制限情報取得               |

Network Service
---------------
| Support Status | Class or Method                                | HTTP Method | URI                                                              | Description                             |
| -------------- | ---------------------------------------------- | ----------- | ---------------------------------------------------------------- | --------------------------------------- |
| not            |                                                | GET         | /                                                                | バージョン情報取得                      |
| not            |                                                | GET         | /v2.0                                                            | バージョン情報詳細取得                  |
| not            |                                                | GET         | /v2.0/networks                                                   | ネットワーク一覧取得                    |
| not            |                                                | GET         | /v2.0/networks/{network\_id}                                     | ネットワーク詳細取得                    |
| not            |                                                | POST        | /v2.0/networks                                                   | ネットワーク追加(ローカルネット用)      |
| not            |                                                | DELETE      | /v2.0/networks/{network\_id}                                     | ネットワーク削除                        |
| not            |                                                | GET         | /v2.0/ports                                                      | ポート一覧取得                          |
| not            |                                                | GET         | /v2.0/ports/{port\_id}                                           | ポート詳細取得                          |
| not            |                                                | POST        | /v2.0/ports/                                                     | ポート追加                              |
| not            |                                                | PUT         | /v2.0/ports/{port\_id}                                           | ポート更新/セキュリティグループ割り当て |
| not            |                                                | DELETE      | /v2.0/ports/{port\_id}                                           | ポート削除                              |
| not            |                                                | GET         | /v2.0/subnets                                                    | サブネット一覧取得                      |
| not            |                                                | GET         | /v2.0/subnets/{subnet\_id}                                       | サブネット詳細取得                      |
| not            |                                                | POST        | /v2.0/subnets                                                    | サブネットの払い出し(ローカルネット用)  |
| not            |                                                | POST        | /v2.0/allocateips                                                | サブネットの払い出し(追加IP用)          |
| not            |                                                | POST        | /v2.0/lb/subnets                                                 | サブネットの払い出し(LB用)              |
| not            |                                                | DELETE      | /v2.0/subnets/{subnet\_id}                                       | サブネットの削除                        |
| not            |                                                | GET         | /v2.0/lb/pools                                                   | POOL一覧取得                            |
| not            |                                                | GET         | /v2.0/lb/pools/{pool\_id}                                        | POOL詳細取得                            |
| not            |                                                | POST        | /v2.0/lb/pools                                                   | POOL追加（バランシング指定）            |
| not            |                                                | PUT         | /v2.0/lb/pools/{pool\_id}                                        | POOL更新(バランシング方式の変更)        |
| not            |                                                | DELETE      | /v2.0/lb/pools/{pool\_id}　                                      | POOL削除                                |
| not            |                                                | GET         | /v2.0/lb/vips                                                    | VIP一覧取得                             |
| not            |                                                | GET         | /v2.0/lb/vips/{vip\_id}                                          | VIP詳細取得                             |
| not            |                                                | POST        | /v2.0/lb/vips                                                    | VIP作成                                 |
| not            |                                                | DELETE      | /v2.0/lb/vips/{vip\_id}                                          | VIP削除                                 |
| not            |                                                | GET         | /v2.0/lb/members                                                 | REAL（member）一覧取得                  |
| not            |                                                | GET         | /v2.0/lb/members/{member\_id}                                    | REAL（member）詳細取得                  |
| not            |                                                | POST        | /v2.0/lb/members                                                 | REAL（member）追加                      |
| not            |                                                | PUT         | /v2.0/lb/members/{member\_id}                                    | REAL(member)起動/停止                   |
| not            |                                                | DELETE      | /v2.0/lb/members/{member\_id}                                    | REAL(member)削除                        |
| not            |                                                | GET         | /v2.0/lb/health\_monitors                                        | ヘルスモニタ一覧取得                    |
| not            |                                                | GET         | /v2.0/lb/health\_monitors/{health\_monitor\_id}                  | ヘルスモニタ詳細取得                    |
| not            |                                                | POST        | /v2.0/lb/health\_monitors                                        | ヘルスモニタ作成                        |
| not            |                                                | PUT         | /v2.0/lb/health\_monitors/{health\_monitor\_id}                  | ヘルスモニタ更新                        |
| not            |                                                | DELETE      | /v2.0/lb/health\_monitors/{health\_monitor\_id}　                | ヘルスモニタ削除                        |
| not            |                                                | POST        | /v2.0/lb/pools/{pool\_id}/health\_monitors                       | ヘルスモニタの関連付け                  |
| not            |                                                | DELETE      | /v2.0/lb/pools/{pool\_id}/health\_monitors/{health\_monitor\_id} | ヘルスモニタの関連付け解除              |
| fully          | network.SecurityGroupList                      | GET         | /v2.0/security-groups                                            | セキュリティグループ一覧取得            |
| not            |                                                | GET         | /v2.0/security-groups/{security\_group\_id}                      | セキュリティグループ詳細取得            |
| fully          | network.SecurityGroupList.add                  | POST        | /v2.0/security-groups                                            | セキュリティグループ作成                |
| fully          | network.SecurityGroup.update{Name,Description} | PUT         | /v2.0/security-groups/{security\_group\_id}                      | セキュリティグループ更新                |
| fully          | network.SecurityGroupList.delete               | DELETE      | /v2.0/security-groups/{security\_group\_id}                      | セキュリティグループ削除                |
| fully          | network.SecurityGroupRuleList                  | GET         | /v2.0/security-group-rules                                       | セキュリティグループ ルール一覧取得     |
| not            |                                                | GET         | /v2.0/security-group-rules/{rules-security-groups-id}            | セキュリティグループ ルール詳細取得     |
| fully          | network.SecurityGroupRuleList.add              | POST        | /v2.0/security-group-rules                                       | セキュリティグループ ルール作成         |
| fully          | network.SecurityGroupRuleList.delete           | DELETE      | /v2.0/security-group-rules/{rules-security-groups-id}            | セキュリティグループ ルール削除         |

Object Storage Service
----------------------
| Support Status | Class or Method | HTTP Method | URI                                    | Description                                                |
| -------------- | --------------- | ----------- | -------------------------------------- | ---------------------------------------------------------- |
| not            |                 | GET         | /v1/nc\_{account}                      | アカウント情報取得                                         |
| not            |                 | POST        | /v1/nc\_{account}                      | アカウントクォータ設定                                     |
| not            |                 | GET         | /v1/nc\_{account}/{container}          | コンテナ情報取得                                           |
| not            |                 | PUT         | /v1/nc\_{account}/{container}          | コンテナ作成                                               |
| not            |                 | DELETE      | /v1/nc\_{account}/{container}          | コンテナ削除                                               |
| not            |                 | GET         | /v1/nc\_{account}/{container}/{object} | オブジェクト情報取得                                       |
| not            |                 | PUT         | /v1/nc\_{account}/{container}/{object} | オブジェクトアップロード                                   |
| not            |                 | PUT         | /v1/nc\_{account}/{container}/{object} | オブジェクトダウンロード                                   |
| not            |                 | COPY        | /v1/nc\_{account}/{container}/{object} | オブジェクト複製                                           |
| not            |                 | DELETE      | /v1/nc\_{account}/{container}/{object} | オブジェクト削除                                           |
| not            |                 | PUT         | /v1/nc\_{account}/{container}/{object} | ラージオブジェクトアップロード(dynamic large objects)      |
| not            |                 | PUT         | /v1/nc\_{account}/{container}/{object} | ラージオブジェクトアップロード(static Large Object)        |
| not            |                 | PUT         | /v1/nc\_{account}/{container}          | オブジェクトバージョン管理(object versioning)              |
| not            |                 | POST        | /v1/nc\_{account}/{container}/{object} | オブジェクトスケジュール削除(schedule objects for deletio) |
| not            |                 | POST        | /v1/nc\_{account}                      | 一時的Web公開(TempURL)                                     |
| not            |                 | POST        | /v1/nc\_{account}/{container}          | Web公開機能(web publishing)                                |

Database Hosting Service
------------------------
| Support Status | Class or Method | HTTP Method | URI                                                     | Description              |
| -------------- | --------------- | ----------- | ------------------------------------------------------- | ------------------------ |
| not            |                 | GET         | /                                                       | バージョン情報取得       |
| not            |                 | GET         | /v1                                                     | バージョン情報詳細取得   |
| not            |                 | POST        | /v1/services                                            | サービス作成             |
| not            |                 | GET         | /v1/services                                            | サービス一覧取得         |
| not            |                 | GET         | /v1/services/(uuid:service\_id)                         | サービス情報取得         |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)                         | サービス更新             |
| not            |                 | DELETE      | /v1/services/(uuid:service\_id)                         | サービス削除             |
| not            |                 | GET         | /v1/services/(uuid:service\_id)/quotas                  | データベース上限値取得   |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)/quotas                  | データベース上限値変更   |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)/action                  | バックアップ有効無効     |
| not            |                 | POST        | /v1/databases                                           | データベース作成         |
| not            |                 | GET         | /v1/databases                                           | データベース一覧取得     |
| not            |                 | GET         | /v1/databases/(uuid:database\_id)                       | データベース情報取得     |
| not            |                 | PUT         | /v1/databases/(uuid:database\_id)                       | データベース更新         |
| not            |                 | DELETE      | /v1/databases/(uuid:database\_id)                       | データベース削除         |
| not            |                 | POST        | /v1/databases/(uuid:database\_id)/grant                 | データベース権限作成     |
| not            |                 | GET         | /v1/databases/(uuid:database\_id)/grant                 | データベース権限一覧取得 |
| not            |                 | DELETE      | /v1/databases/(uuid:database\_id)/grant/(uuid:user\_id) | データベース権限削除     |
| not            |                 | GET         | /v1/databases/(uuid:database\_id)/backup                | バックアップ一覧         |
| not            |                 | POST        | /v1/databases/(uuid:database\_id)/action                | リストア                 |
| not            |                 | POST        | /v1/users                                               | アカウント作成           |
| not            |                 | GET         | /v1/users                                               | アカウント一覧取得       |
| not            |                 | GET         | /v1/users/(uuid:user\_id)                               | アカウント情報取得       |
| not            |                 | PUT         | /v1/users/(uuid:user\_id)                               | アカウント更新           |
| not            |                 | DELETE      | /v1/users/(uuid:user\_id)                               | アカウント削除           |

DNS Service
-----------
| Support Status | Class or Method | HTTP Method | URI                                                     | Description                  |
| -------------- | --------------- | ----------- | ------------------------------------------------------- | ---------------------------- |
| not            |                 | GET         | /                                                       | バージョン情報取得           |
| not            |                 | GET         | /v1/domains/(uuid:domain\_id)/servers                   | ドメインホスティング情報表示 |
| not            |                 | GET         | /v1/domains                                             | ドメイン一覧表示             |
| not            |                 | POST        | /v1/domains                                             | ドメイン作成                 |
| not            |                 | DELETE      | /v1/domains/(uuid:domain\_id)                           | ドメイン削除                 |
| not            |                 | GET         | /v1/domains/(uuid:domain\_id)                           | ドメイン情報表示             |
| not            |                 | PUT         | /v1/domains/(uuid:domain\_id)                           | ドメイン更新                 |
| not            |                 | GET         | /v1/domains/(uuid:domain\_id)/records                   | レコード一覧取得             |
| not            |                 | POST        | /v1/domains/(uuid:domain\_id)/records                   | レコード作成                 |
| not            |                 | DELETE      | /v1/domains/(uuid:domain\_id)/records/(uuid:record\_id) | レコード削除                 |
| not            |                 | GET         | /v1/domains/(uuid:domain\_id)/records/(uuid:record\_id) | レコード情報表示             |
| not            |                 | PUT         | /v1/domains/(uuid:domain\_id)/records/(uuid:record\_id) | レコード更新                 |
| not            |                 | POST        | /v2/zones                                               | ゾーンファイルインポート     |
| not            |                 | GET         | /v2/zones/(uuid:id)                                     | ゾーンファイルエクスポート   |

Mail Hosting Service
--------------------
| Support Status | Class or Method | HTTP Method | URI                                                                                       | Description                           |
| -------------- | --------------- | ----------- | ----------------------------------------------------------------------------------------- | ------------------------------------- |
| not            |                 | GET         | /                                                                                         | バージョン情報取得                    |
| not            |                 | GET         | /v1                                                                                       | バージョン情報詳細取得                |
| not            |                 | POST        | /v1/services                                                                              | サービス作成                          |
| not            |                 | GET         | /v1/services                                                                              | サービス一覧取得                      |
| not            |                 | GET         | /v1/services/(uuid:service\_id)                                                           | サービス情報取得                      |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)                                                           | サービス更新                          |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)/action                                                    | バックアップ(有効/無効)               |
| not            |                 | DELETE      | /v1/services/(uuid:service\_id)                                                           | サービス削除                          |
| not            |                 | GET         | /v1/services/(uuid:service\_id)/quotas                                                    | メール上限値取得                      |
| not            |                 | PUT         | /v1/services/(uuid:service\_id)/quotas                                                    | メール上限値変更                      |
| not            |                 | POST        | /v1/domains                                                                               | ドメイン作成                          |
| not            |                 | GET         | /v1/domains                                                                               | ドメイン一覧取得                      |
| not            |                 | DELETE      | /v1/domains/(uuid:domain\_id)                                                             | ドメイン削除                          |
| not            |                 | GET         | /v1/domains/(uuid:domain\_id)/dedicatedip                                                 | ドメインの個別IP割り当て情報取得      |
| not            |                 | PUT         | /v1/domains/(uuid:domain\_id)/action                                                      | ドメインの個別IP割り当て（登録/解除） |
| not            |                 | POST        | /v1/emails                                                                                | メールアドレス作成                    |
| not            |                 | GET         | /v1/emails                                                                                | メールアドレス一覧取得                |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)                                                               | メールアドレス情報取得                |
| not            |                 | DELETE      | /v1/emails/(uuid:email\_id)                                                               | メールアドレス削除                    |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/password                                                      | メールアドレスパスワード変更          |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/action                                                        | 迷惑メールフィルタ（有効/無効）       |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/action                                                        | メール転送設定変更                    |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/messages                                                      | メッセージ一覧取得                    |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/messages/(uuid:message\_id)                                   | メッセージ取得                        |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/messages/(uuid:message\_id)/attachments/(uuid:attachment\_id) | メッセージ添付ファイル取得            |
| not            |                 | DELETE      | /v1/emails/(uuid:email\_id)/messages/(uuid:message\_id)                                   | メッセージ削除                        |
| not            |                 | POST        | /v1/emails/(uuid:email\_id)/webhook                                                       | 自動実行作成                          |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/webhook                                                       | 自動実行情報取得                      |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/webhook                                                       | 自動実行更新                          |
| not            |                 | DELETE      | /v1/emails/(uuid:email\_id)/webhook                                                       | 自動実行削除                          |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/whitelist                                                     | 迷惑メールフィルタ許可一覧取得        |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/whitelist                                                     | 迷惑メールフィルタ許可リスト更新      |
| not            |                 | GET         | /v1/emails/(uuid:email\_id)/blacklist                                                     | 迷惑メールフィルタ拒否一覧取得        |
| not            |                 | PUT         | /v1/emails/(uuid:email\_id)/blacklist                                                     | 迷惑メールフィルタ拒否リスト更新      |
| not            |                 | POST        | /v1/forwarding                                                                            | メール転送先追加                      |
| not            |                 | GET         | /v1/forwarding                                                                            | メール転送先一覧取得                  |
| not            |                 | GET         | /v1/forwarding/(uuid:forwarding\_id)                                                      | メール転送先情報取得                  |
| not            |                 | PUT         | /v1/forwarding/(uuid:forwarding\_id)                                                      | メール転送先変更                      |
| not            |                 | DELETE      | /v1/forwarding/(uuid:forwarding\_id)                                                      | メール転送先解除                      |

