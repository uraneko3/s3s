s3s for lambda
=====
を作成中。いちおう動いたっぽい。

前提
=====
以下のような方向け。
- 本家のs3sがなにをしてるかある程度わかっている
- Lambda へ zip で manual upload して必要な設置ができる
  - Setupには Local な Python3 環境が必要
- S3 や LambdaからS3の操作に必要な IAM 権限についてある程度分かってる前提（ここでは詳しく書かない）

※セットアップは、 S3 への config.txt の保存を想定しているので、aws EC2 上で使うと楽かも。t3.nano の spot とかだい>ぶ安価のはず（それでtest済み）
※S3テスト部分を省くのであれば、どのような環境でもダイジョブのはず。

想定使用イメージ
====
- Local の python3 環境に git clone
- ごそごそと必要なことをして zip で固める
- zip を Lambda に上げて動かす
- それだけ


使い方のイメージ
=====
- `git clone` して requirement.txt を install (`pip3 install -r requirements.txt`)
- `s3s.py -t` でconfig.txt 生成 (本来は同じディレクトリにできるが、ここでは /tmp　配下にできる)　※手順は本家と同じ
  - (念のため `s3s.py -r` で自分の stat.ink を更新できるか確認してもよい)
- S3 bucket のディレクトリ内に config.txt を upload しておく
- lambda_function.py の中の　**<input your S3 bucket name>** と **<input your S3 directory name>**　を部分を、自身S3のものに変更する
  - 例：
  - `S3_BUCKET = "uranekoS3bucket"`
  - `S3_DIR = "s3s-config"`
- Lambda で動くように、 必要な package をカレントディレクトリに置く (`pip3 install -r requirements.txt -t .`)
- (この時点で lambda_function.py のテストをする場合、boto3 の install が必要 (`pip3 install boto3`)　
    - ※Lambda 上では boto3 不要なので `-t .` 不要
- zip で固める　(`zip -r ../myLambdaS3sPack.zip ./*`)

- できた zip を Lambda に上げて、ハンドラ指定して(lambda_function.main) 、ロールにS3操作権限付与して、トリガー設定>して、timeout を2分に変えておく(1分でもたぶんダイジョブ)

※Local環境が共有環境の場合には、テストがおわったら/tmp/config.txtは消しておくと良いでしょう。


本家からの差分
====
### s3s.py
- app_path を /tmp に変更
- これにより config.txt の保存先が /tmp/config.txt になる
  - (Lambda 上でのファイルの読み書きを可能にするため)

### lambda_function.py (new file)
- lambda 用のハンドラ
- S3 bucket から config.txt をダウンロードして /tmp に置く
- s3s.py　実行
- /tmp/config.txt を S3 bucket へアップロード
- それだけ


フォーク元
=====
frozenpandaman/s3s
