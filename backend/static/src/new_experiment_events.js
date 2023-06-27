$(document).ready(function () {
    $("div.desc").hide();
    document.getElementById("demo").innerHTML = text;
    $("input[name$='methodology' ]").click(function () {
        var test = $(this).val();
        var num = 0
        var count = 1
        const Methodologies = ["LCA:", "MLA:"]

        for (const methodology of Methodologies) {
            if (test == methodology) {
                num = count
            }
            count = count + 1
        }
        $("div.desc").hide();
        $("#LoadData" + num).show();
    });
});