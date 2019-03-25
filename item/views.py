from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from item.models import Shou, Prob, Shintyoku
from django.urls import reverse
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin


class Top_page(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user_name = request.user.get_username
        shou_kensu = Shou.objects.filter().count()
        shou_name = Shou.objects.all()
        shou_num = int(Shou.objects.all()[0].id)

        mondai_kensu = []
        for i in range(shou_kensu):
            kensu_ = Prob.objects.filter(shou_id=shou_num).count()
            mondai_kensu.append(kensu_)
            shintyoku_kensu = []
            shintyoku_ritsu = []
            seikai_ritsu = []
            shou_num += 10

        shou_num = int(Shou.objects.all()[0].id)
        for i in range(shou_kensu):
            kensu_ = Shintyoku.objects.filter(kaiin_id=user_id, shou_id=shou_num).count()
            shintyoku_kensu.append(kensu_)

            if mondai_kensu[i] != 0:
                shintyoku_ritsu.append(int(round(shintyoku_kensu[i]/mondai_kensu[i],2)*100))
            else:
                shintyoku_ritsu.append(0)

            正解数 = Shintyoku.objects.filter(kaiin_id=user_id, shou_id=shou_num, seigo='正解').count()
            不正解数 = Shintyoku.objects.filter(kaiin_id=user_id, shou_id=shou_num, seigo='不正解').count()

            try:
                seikai_ritsu_ = 正解数/(正解数 + 不正解数)
                seikai_ritsu.append(int(round(seikai_ritsu_*100,2)))
            except:
                if 不正解数 == 0:
                    if 正解数 == 0:
                        seikai_ritsu.append(0)
                    else:
                        seikai_ritsu.append(100)

            shou_num += 10

        ritsu = []
        shou_num = int(Shou.objects.all()[0].id)
        for i in range(len(seikai_ritsu)):
            ritsu_ = []
            ritsu_.append(shou_num)
            ritsu_.append(i + 1)
            ritsu_.append(shou_name[i].shou_name)
            ritsu_.append(shintyoku_ritsu[i])
            ritsu_.append(seikai_ritsu[i])
            ritsu.append(ritsu_)
            shou_num += 10

        context = {'user_id':user_id, 'user_name':user_name,\
                'shintyoku_ritsu':shintyoku_ritsu, 'seikai_ritsu':seikai_ritsu, 'ritsu':ritsu}

        return render(request, 'item/top_page.html', context=context)

top_page = Top_page.as_view()

class Prob_list(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        shou_id_ = kwargs['shou_id']
        user_id = request.user.id
        probs = Prob.objects.filter(shou_id=shou_id_)
        # FreignFieldが指定されているTableとのJoin句
        shintyokus = Shintyoku.objects.filter(kaiin_id=user_id, shou_id=shou_id_).select_related()

        statuses = []
        for prob in probs:
            prob_num = prob.prob_num
            prob_title = prob.title
            i = 0
            for shintyoku in shintyokus:
                if prob_num == shintyoku.prob.prob_num:
                    prob_status = shintyoku.seigo
                    i += 1

            if i == 0:
                statuses.append({'prob_num':prob_num, 'prob_title':prob_title, 'prob_status':'未回答'})
            else:
                statuses.append({'prob_num':prob_num, 'prob_title':prob_title, 'prob_status':prob_status})


        shou_name = Shou.objects.filter(id = shou_id_)[0].shou_name


        context = {'statuses':statuses, 'shou_id_':shou_id_, 'shou_id':int((shou_id_ - 2)/10), 'shou_name':shou_name}
        return render(request, 'item/prob_list.html', context=context)

prob_list = Prob_list.as_view()

class Answer_page(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        shou_id_ = kwargs['shou_id']
        prob_num = kwargs['prob_num']

        try:
            prob_ = Prob.objects.filter(shou_id=shou_id_, prob_num=prob_num)[0]
            context = {'prob_':prob_, 'prob_num':prob_num, 'shou_id':shou_id_}
            return render(request, 'item/answer_page.html', context=context)
        except:
            shou_id_max = Shou.objects.all().order_by('-id')[0].id
            if shou_id_ != shou_id_max:
                shou_id_ = shou_id_ + 10
                prob_num = 1
                return redirect(reverse('item:answer_page', args=[shou_id_ ,prob_num]))
            else:
                shou_id_ = Shou.objects.all().order_by('id')[0].id
                prob_num = 1
                return redirect(reverse('item:answer_page', args=[shou_id_ ,prob_num]))


    def post(self, request, *args, **kwargs):
        answer = int(request.POST.getlist('選択肢')[0])
        shou_id = kwargs['shou_id']
        prob_num = int(kwargs['prob_num'])
        next_id = prob_num + 1
        prob = Prob.objects.filter(shou_id=shou_id, prob_num=prob_num)[0]
        true_ = prob.seikai
        if true_ == answer:
            seigo = '正解'
        else:
            seigo = '不正解'

        shou_id = Prob.objects.filter(shou_id= shou_id, prob_num=prob_num).select_related()[0].shou_id
        prob_id = Prob.objects.filter(shou_id= shou_id, prob_num=prob_num)[0].id

        try:
            id = Shintyoku.objects.filter(prob_id=prob_id, shou_id=shou_id, kaiin_id=request.user.id).select_related()[0].id
            query_ = Shintyoku.objects.get(id=id)
            query_.seigo = seigo
            query_.save()
        except:
            query_ = Shintyoku(seigo=seigo, answer_date=datetime.date.today(), kaiin_id=request.user.id, prob_id=prob_id, shou_id=shou_id)
            query_.save()

        context = {'answer':answer,'shou_id':shou_id, 'prob_num':prob_num, 'prob':prob, 'seigo':seigo, 'next_id':next_id, 'true_':true_}

        return render(request, 'item/answer_check.html', context=context)

answer_page = Answer_page.as_view()
