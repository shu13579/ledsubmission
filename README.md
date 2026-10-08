# Devoxx LED — Japan × Belgium × Java

応募用のオリジナル・ピクセルアニメーション3本。写真の縮小ではなく、64×64の座標上で構図・立体投影・動きをプログラムしています。

| 提出ファイル | 内容 |
| --- | --- |
| `submissions/01-japan-belgium-express.gif` | **Across the Seas — Japan to Antwerp**。文字を使わず、左の富士山・鳥居・日の丸と右の中央駅・ベルギー旗を同じ大きさの旗で結ぶ。白い飛行機は空の弧を一定速度で左から右へ渡り、姿勢は滑らかな微分から計算して±20度に制限。両端は画面外なのでループの巻き戻りは見えません。駅のドーム・飾り塔・時計・窓格子・左右の小塔・石壁の陰影も描写。実際の景観・地理・飛行経路を再現したものではありません。ファイル名は差し替えのため以前の名前を維持しています。 |
| `submissions/02-java-steam-to-code.gif` | 日ベルの旗を載せたJavaコーヒー。湯気の中をコード記号が上昇し、床の回路には光のパケットが流れる。 |
| `submissions/03-devoxx-atomium-portal.gif` | 鳥居のポータル内で9球のAtomiumが3D回転。奥行き順の描画、20本の接続、軌道上の光、中心からの通信。 |

**提出するのは `submissions/` 内の3つのGIFです。** 全て64×64、128フレーム、80ms/フレーム、10.24秒、無限ループ、5MB未満。`previews/` の512×512 GIFは拡大確認用です。`preview.html` をブラウザーで開くと3作品のアニメーションを比較できます。

## 再生成

必要: Python 3 + Pillow (`pip install pillow`)、Java 17以上のJDK、Git、Maven。

```powershell
powershell -ExecutionPolicy Bypass -File .\build-jixoo.ps1 -Python python
```

1. `generate.py` が全作品のRGBフレームを生成。作品ごとに共通128色パレットを構成し、ディザリングせずLED上のちらつきを抑えます。
2. スクリプトは **glaforge/jixoo を clone** し、コミット `2703d703d7db530a74555b403f3a4a39f6383b55` に固定。上流の画像関連10クラスを変更せずコンパイルします。
3. `JixooExport.java` が実際に Jixoo の `PixooFrame` / `PixooAnimation` / `GifEncoder.encode` で最終GIFを生成します。フルのネットワーククライアントやCLIは使いません。
4. `verify.py` がPillowの別デコーダーで全GIFを読み、元のRGBと全フレーム全ピクセルが一致すること、サイズ・容量・ループ・色数・継ぎ目を検証します。

`validation.json` が検証結果、`manifest.json` が作品仕様です。`work/` は再生成時の一時ファイルでGit対象外です。

## Credits

- 構図・ピクセルアート・アニメーション・3D投影: 本プロジェクトのオリジナルコード `generate.py`。外部画像、公式ロゴのコピー、生成AI画像は使用していません。
- GIFエンコード: [Jixoo / glaforge](https://github.com/glaforge/jixoo)、Apache-2.0。
- 描画・パレット・独立した検証: [Pillow](https://python-pillow.github.io/)、HPND。
- Atomiumの形状参考: [公式 Shape of the Atomium](https://atomium.be/the_shape_of_the_atomium?lang=en)、[公式 figures](https://atomium.be/the_atomium_in_figures)。絵は独自のピクセル描画です。
- アントワープ中央駅の参考: [NMBS公式駅ページ](https://www.belgiantrain.be/station-information/antwerpen/antwerpen-centraal)、[市の建築照明紹介](https://pers.antwerpen.be/nieuwe-gevelverlichting-zet-station-antwerpen-centraal-elisabethzaal-en-ingang-zoo-in-de-verf)。写真の転載ではなく、特徴を独自のピクセルで描いた作品です。
- テーマ: [Devoxx Belgium](https://www.devoxx.be/)。本作品は非公式の応募作品で、主催者やJava商標権者との提携を示すものではありません。

オリジナルコードのライセンスはMIT、オリジナルアートは本プロジェクトと共に使用・改変・提出できます。第三者のライブラリと商標にはそれぞれの権利が適用されます。
